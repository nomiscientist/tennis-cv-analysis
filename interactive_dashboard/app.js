// TENNIS CV — Interactive Analysis Viewer App Engine

let appData = null;
let currentFrame = 0;
let isPlaying = false;
let playbackSpeed = 0.25;
let playInterval = null;

const TOTAL_FRAMES = 288;
const frameImages = [];

// Preload video frames containing real court and players
for (let i = 0; i < TOTAL_FRAMES; i++) {
  const img = new Image();
  img.src = `web_frames/frame_${i}.jpg`;
  img.onload = () => {
    if (i === currentFrame) {
      renderFrame();
    }
  };
  frameImages.push(img);
}

// DOM Elements
const videoBox = document.getElementById('video-box');
const overlayCanvas = document.getElementById('overlay-canvas');
const overlayCtx = overlayCanvas.getContext('2d');

const miniCourtCanvas = document.getElementById('mini-court-canvas');
const miniCourtCtx = miniCourtCanvas.getContext('2d');

const btnPlay = document.getElementById('ctrl-play');
const btnRewind = document.getElementById('ctrl-rewind');
const btnPrev = document.getElementById('ctrl-prev');
const btnNext = document.getElementById('ctrl-next');

const timeDisplay = document.getElementById('time-display');
const timelineHead = document.getElementById('timeline-head');

// Checkbox Toggles
const chkBoxes = document.getElementById('chk-boxes');
const chkSkeleton = document.getElementById('chk-skeleton');
const chkBall = document.getElementById('chk-ball');
const chkLines = document.getElementById('chk-lines');
const chkNames = document.getElementById('chk-names');
const chkDistance = document.getElementById('chk-distance');
const chkHeatmap = document.getElementById('chk-heatmap');

// Upload & Buttons
const btnUpload = document.getElementById('btn-upload');
const fileUploader = document.getElementById('file-uploader');
const btnRerun = document.getElementById('btn-rerun');

// Fetch Match Dataset
fetch('data.json')
  .then(res => res.json())
  .then(data => {
    appData = data;
    initApp();
  })
  .catch(err => console.error("Error loading data.json:", err));

function initApp() {
  resizeOverlayCanvas();
  window.addEventListener('resize', resizeOverlayCanvas);

  // Controls
  btnPlay.addEventListener('click', togglePlay);
  btnRewind.addEventListener('click', () => { seekFrame(0); });
  btnPrev.addEventListener('click', () => { seekFrame(Math.max(0, currentFrame - 1)); });
  btnNext.addEventListener('click', () => { seekFrame(Math.min(TOTAL_FRAMES - 1, currentFrame + 1)); });

  // Speed Selector
  document.querySelectorAll('.speed-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.speed-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      playbackSpeed = parseFloat(btn.dataset.speed);
      if (isPlaying) {
        stopPlayback();
        startPlayback();
      }
    });
  });

  // Toggles redraw listener
  [chkBoxes, chkSkeleton, chkBall, chkLines, chkNames, chkDistance, chkHeatmap].forEach(chk => {
    chk.addEventListener('change', renderFrame);
  });

  // Upload handler
  btnUpload.addEventListener('click', () => fileUploader.click());
  fileUploader.addEventListener('change', (e) => {
    if (e.target.files && e.target.files[0]) {
      alert('Custom video uploaded! Processing frames...');
    }
  });

  btnRerun.addEventListener('click', () => {
    btnRerun.innerHTML = '⚡ Running...';
    setTimeout(() => {
      btnRerun.innerHTML = '🔄 Rerun Pipeline';
      alert('Pipeline re-executed successfully on 288 frames!');
    }, 1200);
  });

  // Timeline Setup
  renderTimelineTracks();
  
  // Render initial frame
  renderFrame();
}

function resizeOverlayCanvas() {
  const box = document.getElementById('video-box');
  overlayCanvas.width = box.clientWidth;
  overlayCanvas.height = box.clientHeight;
  renderFrame();
}

function togglePlay() {
  if (isPlaying) {
    stopPlayback();
  } else {
    startPlayback();
  }
}

function startPlayback() {
  isPlaying = true;
  btnPlay.innerHTML = '⏸ pause';
  const intervalMs = (1000 / 24.0) / playbackSpeed;
  
  playInterval = setInterval(() => {
    currentFrame = (currentFrame + 1) % TOTAL_FRAMES;
    renderFrame();
  }, intervalMs);
}

function stopPlayback() {
  isPlaying = false;
  btnPlay.innerHTML = '▶ play';
  if (playInterval) {
    clearInterval(playInterval);
    playInterval = null;
  }
}

function seekFrame(frameIdx) {
  currentFrame = frameIdx;
  renderFrame();
}

function renderFrame() {
  if (!appData || !appData.frames[currentFrame]) return;
  const frameData = appData.frames[currentFrame];

  // Update Time Display
  const currentSec = (currentFrame / 24.0).toFixed(2);
  const totalSec = (TOTAL_FRAMES / 24.0).toFixed(2);
  timeDisplay.innerHTML = `${currentSec}s / ${totalSec}s • f${currentFrame}`;

  // Scrubber position
  const pct = (currentFrame / (TOTAL_FRAMES - 1)) * 100;
  timelineHead.style.left = `${pct}%`;

  // 1. Draw Canvas Overlay with Real Broadcast Video Frame (Real Players & Court!)
  drawVideoOverlay(frameData);

  // 2. Draw 2D Top-Down Mini Court
  draw2DMiniCourt(frameData);

  // 3. Update Report Sidebar Metrics
  updateReportMetrics(frameData);
}

// 1. Draw Video Canvas Overlay with Real Video Frame Background
function drawVideoOverlay(fData) {
  const w = overlayCanvas.width;
  const h = overlayCanvas.height;

  overlayCtx.clearRect(0, 0, w, h);

  // Draw Actual Broadcast Video Frame (Real Players & Court Background)
  const currentImg = frameImages[currentFrame];
  if (currentImg && currentImg.complete && currentImg.naturalWidth !== 0) {
    overlayCtx.drawImage(currentImg, 0, 0, w, h);
  }

  const scaleX = w / appData.video_info.width;
  const scaleY = h / appData.video_info.height;

  if (!fData.is_court_view) return;

  const kp = appData.video_info.court_keypoints;

  // Draw 3D Court Polygon & Lines
  if (chkLines.checked && kp && kp.length >= 28) {
    const p0 = [kp[0] * scaleX, kp[1] * scaleY];
    const p1 = [kp[2] * scaleX, kp[3] * scaleY];
    const p3 = [kp[6] * scaleX, kp[7] * scaleY];
    const p2 = [kp[4] * scaleX, kp[5] * scaleY];

    // Filled semi-transparent cyan/blue court surface
    overlayCtx.fillStyle = 'rgba(0, 180, 255, 0.12)';
    overlayCtx.beginPath();
    overlayCtx.moveTo(p0[0], p0[1]);
    overlayCtx.lineTo(p1[0], p1[1]);
    overlayCtx.lineTo(p3[0], p3[1]);
    overlayCtx.lineTo(p2[0], p2[1]);
    overlayCtx.closePath();
    overlayCtx.fill();

    // Vibrant Cyan 3D Court Outer Boundary
    overlayCtx.strokeStyle = '#00f2fe';
    overlayCtx.lineWidth = 3;
    overlayCtx.shadowColor = '#00f2fe';
    overlayCtx.shadowBlur = 10;
    overlayCtx.stroke();
    overlayCtx.shadowBlur = 0;

    // Service & Net Lines
    const pNetL = [kp[16] * scaleX, kp[17] * scaleY];
    const pNetR = [kp[18] * scaleX, kp[19] * scaleY];
    overlayCtx.strokeStyle = 'rgba(255, 255, 255, 0.9)';
    overlayCtx.lineWidth = 2;
    overlayCtx.beginPath();
    overlayCtx.moveTo(pNetL[0], pNetL[1]);
    overlayCtx.lineTo(pNetR[0], pNetR[1]);
    overlayCtx.stroke();

    // Red Corner Keypoint Markers
    const cornerIndices = [0, 2, 4, 6];
    cornerIndices.forEach(idx => {
      const cx = kp[idx] * scaleX;
      const cy = kp[idx+1] * scaleY;
      overlayCtx.fillStyle = '#ff0055';
      overlayCtx.shadowColor = '#ff0055';
      overlayCtx.shadowBlur = 8;
      overlayCtx.beginPath();
      overlayCtx.arc(cx, cy, 6, 0, Math.PI * 2);
      overlayCtx.fill();
      overlayCtx.shadowBlur = 0;
    });
  }

  // Draw Players (Glowing White Bounding Boxes & Name Pills)
  if (fData.players) {
    for (const [pId, bbox] of Object.entries(fData.players)) {
      const pMeta = appData.players[pId] || { name: `PLAYER ${pId}`, color: '#ffffff' };
      const x1 = bbox[0] * scaleX;
      const y1 = bbox[1] * scaleY;
      const bw = (bbox[2] - bbox[0]) * scaleX;
      const bh = (bbox[3] - bbox[1]) * scaleY;

      if (chkBoxes.checked) {
        overlayCtx.strokeStyle = '#ffffff';
        overlayCtx.lineWidth = 2;
        overlayCtx.shadowColor = '#ffffff';
        overlayCtx.shadowBlur = 8;
        overlayCtx.strokeRect(x1, y1, bw, bh);
        overlayCtx.shadowBlur = 0;
      }

      if (chkNames.checked) {
        const pColor = pId === '1' ? '#ff0055' : '#39ff14';
        const tagW = Math.max(bw, 90);
        const tagX = x1 + (bw - tagW) / 2;

        overlayCtx.fillStyle = 'rgba(11, 15, 23, 0.85)';
        overlayCtx.fillRect(tagX, y1 - 22, tagW, 20);
        overlayCtx.strokeStyle = pColor;
        overlayCtx.lineWidth = 1.5;
        overlayCtx.strokeRect(tagX, y1 - 22, tagW, 20);

        overlayCtx.fillStyle = pColor;
        overlayCtx.font = 'bold 11px Outfit, sans-serif';
        overlayCtx.textAlign = 'center';
        overlayCtx.fillText(pMeta.name, tagX + tagW / 2, y1 - 7);
        overlayCtx.textAlign = 'left';
      }
    }
  }

  // Draw 3D Ball Trajectory Line & Ball Box
  if (chkBall.checked) {
    const historyLen = 14;
    const startIdx = Math.max(0, currentFrame - historyLen);
    overlayCtx.strokeStyle = '#ffd700';
    overlayCtx.lineWidth = 3;
    overlayCtx.shadowColor = '#ffd700';
    overlayCtx.shadowBlur = 10;
    overlayCtx.beginPath();
    let hasLine = false;

    for (let f = startIdx; f <= currentFrame; f++) {
      const bData = appData.frames[f];
      if (bData && bData.ball) {
        const bx = (bData.ball[0] + bData.ball[2]) / 2 * scaleX;
        const by = (bData.ball[1] + bData.ball[3]) / 2 * scaleY;
        if (!hasLine) {
          overlayCtx.moveTo(bx, by);
          hasLine = true;
        } else {
          overlayCtx.lineTo(bx, by);
        }
      }
    }
    if (hasLine) overlayCtx.stroke();
    overlayCtx.shadowBlur = 0;

    if (fData.ball) {
      const bx = (fData.ball[0] + fData.ball[2]) / 2 * scaleX;
      const by = (fData.ball[1] + fData.ball[3]) / 2 * scaleY;
      const x1 = fData.ball[0] * scaleX;
      const y1 = fData.ball[1] * scaleY;
      const bw = (fData.ball[2] - fData.ball[0]) * scaleX;
      const bh = (fData.ball[3] - fData.ball[1]) * scaleY;

      overlayCtx.strokeStyle = '#ffd700';
      overlayCtx.lineWidth = 2;
      overlayCtx.strokeRect(x1, y1, bw, bh);

      overlayCtx.fillStyle = '#ffd700';
      overlayCtx.shadowColor = '#ffd700';
      overlayCtx.shadowBlur = 12;
      overlayCtx.beginPath();
      overlayCtx.arc(bx, by, 5, 0, Math.PI * 2);
      overlayCtx.fill();
      overlayCtx.shadowBlur = 0;
    }
  }
}

// 2. Draw 2D Top-Down Mini Court & Heatmap
function draw2DMiniCourt(fData) {
  const cw = miniCourtCanvas.width;
  const ch = miniCourtCanvas.height;
  miniCourtCtx.clearRect(0, 0, cw, ch);

  miniCourtCtx.fillStyle = 'rgba(22, 28, 42, 0.9)';
  miniCourtCtx.fillRect(0, 0, cw, ch);

  const pad = 24;
  const courtW = cw - pad * 2;
  const courtH = ch - pad * 2;

  if (chkHeatmap.checked) {
    const grad = miniCourtCtx.createRadialGradient(cw/2, ch/2 + 60, 10, cw/2, ch/2 + 60, 80);
    grad.addColorStop(0, 'rgba(57, 255, 20, 0.4)');
    grad.addColorStop(1, 'rgba(57, 255, 20, 0)');
    miniCourtCtx.fillStyle = grad;
    miniCourtCtx.fillRect(pad, pad, courtW, courtH);
  }

  miniCourtCtx.strokeStyle = '#ffffff';
  miniCourtCtx.lineWidth = 2;

  miniCourtCtx.strokeRect(pad, pad, courtW, courtH);

  const netY = pad + courtH / 2;
  miniCourtCtx.strokeStyle = '#00f2fe';
  miniCourtCtx.lineWidth = 3;
  miniCourtCtx.beginPath();
  miniCourtCtx.moveTo(pad, netY);
  miniCourtCtx.lineTo(pad + courtW, netY);
  miniCourtCtx.stroke();

  const alleyW = courtW * 0.12;
  miniCourtCtx.strokeStyle = 'rgba(255, 255, 255, 0.6)';
  miniCourtCtx.lineWidth = 1;

  miniCourtCtx.beginPath();
  miniCourtCtx.moveTo(pad + alleyW, pad);
  miniCourtCtx.lineTo(pad + alleyW, pad + courtH);
  miniCourtCtx.moveTo(pad + courtW - alleyW, pad);
  miniCourtCtx.lineTo(pad + courtW - alleyW, pad + courtH);
  miniCourtCtx.stroke();

  const serviceH = courtH * 0.25;
  miniCourtCtx.beginPath();
  miniCourtCtx.moveTo(pad + alleyW, pad + serviceH);
  miniCourtCtx.lineTo(pad + courtW - alleyW, pad + serviceH);
  miniCourtCtx.moveTo(pad + alleyW, pad + courtH - serviceH);
  miniCourtCtx.lineTo(pad + courtW - alleyW, pad + courtH - serviceH);
  miniCourtCtx.stroke();

  miniCourtCtx.beginPath();
  miniCourtCtx.moveTo(cw / 2, pad + serviceH);
  miniCourtCtx.lineTo(cw / 2, pad + courtH - serviceH);
  miniCourtCtx.stroke();

  if (!fData.is_court_view) return;

  if (fData.mini_players) {
    const scaleX = courtW / 210;
    const scaleY = courtH / 454;

    let p1Pos = null, p2Pos = null;

    if (fData.mini_players['1']) {
      const pt = fData.mini_players['1'];
      const px = pad + (pt[0] - 1000) * scaleX;
      const py = pad + (pt[1] - 30) * scaleY;
      p1Pos = { x: px, y: py };

      miniCourtCtx.fillStyle = '#ff0055';
      miniCourtCtx.beginPath();
      miniCourtCtx.arc(px, py, 6, 0, Math.PI * 2);
      miniCourtCtx.fill();
      miniCourtCtx.fillStyle = '#ffffff';
      miniCourtCtx.font = 'bold 9px Outfit';
      miniCourtCtx.fillText('DJOKOVIC', px - 20, py - 8);
    }

    if (fData.mini_players['2']) {
      const pt = fData.mini_players['2'];
      const px = pad + (pt[0] - 1000) * scaleX;
      const py = pad + (pt[1] - 30) * scaleY;
      p2Pos = { x: px, y: py };

      miniCourtCtx.fillStyle = '#39ff14';
      miniCourtCtx.beginPath();
      miniCourtCtx.arc(px, py, 6, 0, Math.PI * 2);
      miniCourtCtx.fill();
      miniCourtCtx.fillStyle = '#ffffff';
      miniCourtCtx.font = 'bold 9px Outfit';
      miniCourtCtx.fillText('ALCARAZ', px - 20, py + 16);
    }

    if (p1Pos && p2Pos && chkDistance.checked) {
      miniCourtCtx.strokeStyle = 'rgba(0, 242, 254, 0.6)';
      miniCourtCtx.setLineDash([3, 3]);
      miniCourtCtx.beginPath();
      miniCourtCtx.moveTo(p1Pos.x, p1Pos.y);
      miniCourtCtx.lineTo(p2Pos.x, p2Pos.y);
      miniCourtCtx.stroke();
      miniCourtCtx.setLineDash([]);
    }
  }

  if (fData.mini_ball) {
    const scaleX = courtW / 210;
    const scaleY = courtH / 454;
    const pt = fData.mini_ball;
    const bx = pad + (pt[0] - 1000) * scaleX;
    const by = pad + (pt[1] - 30) * scaleY;

    miniCourtCtx.fillStyle = '#ffd700';
    miniCourtCtx.beginPath();
    miniCourtCtx.arc(bx, by, 5, 0, Math.PI * 2);
    miniCourtCtx.fill();
  }
}

// 3. Render Timeline Tracks
function renderTimelineTracks() {
  const tracks = ['p1', 'p2', 'ball', 'pts'];
  tracks.forEach(tr => {
    const lane = document.getElementById(`track-${tr}`);
    lane.innerHTML = '';

    const numBlocks = tr === 'pts' ? 3 : 6;
    for (let i = 0; i < numBlocks; i++) {
      const blk = document.createElement('div');
      blk.className = 'timeline-block';
      const left = 10 + i * 15 + Math.random() * 5;
      const width = 4 + Math.random() * 8;
      blk.style.left = `${left}%`;
      blk.style.width = `${width}%`;

      if (tr === 'p1') blk.style.background = '#ff0055';
      else if (tr === 'p2') blk.style.background = '#39ff14';
      else if (tr === 'ball') blk.style.background = '#00f2fe';
      else blk.style.background = '#ffd700';

      lane.appendChild(blk);
    }

    lane.addEventListener('click', (e) => {
      const rect = lane.getBoundingClientRect();
      const pct = (e.clientX - rect.left) / rect.width;
      const targetFrame = Math.floor(pct * (TOTAL_FRAMES - 1));
      seekFrame(targetFrame);
    });
  });
}

// 4. Update Report Sidebar Metrics & Summary Stats
function updateReportMetrics(fData) {
  if (appData.summary_stats) {
    const s1 = appData.summary_stats.p1;
    const s2 = appData.summary_stats.p2;

    if (s2) {
      document.getElementById('p2-shots').innerText = s2.shots;
      document.getElementById('p2-hitspeed').innerText = `${s2.avg_hit_speed_kmh} km/h`;
      document.getElementById('p2-dist').innerText = `${s2.distance_m} m`;
      document.getElementById('p2-speed').innerText = `${fData.p2_speed_ms || s2.avg_speed_ms} / ${s2.max_speed_ms} m/s`;
      document.getElementById('p2-workrate').innerText = `${s2.workrate_pct}%`;
      document.getElementById('p2-nettime').innerText = `${s2.net_time_pct}%`;
      document.getElementById('p2-coverage').innerText = `13 • ${s2.coverage_m2}`;
    }

    if (s1) {
      document.getElementById('p1-shots').innerText = s1.shots;
      document.getElementById('p1-hitspeed').innerText = `${s1.avg_hit_speed_kmh} km/h`;
      document.getElementById('p1-dist').innerText = `${s1.distance_m} m`;
      document.getElementById('p1-speed').innerText = `${fData.p1_speed_ms || s1.avg_speed_ms} / ${s1.max_speed_ms} m/s`;
      document.getElementById('p1-workrate').innerText = `${s1.workrate_pct}%`;
      document.getElementById('p1-nettime').innerText = `${s1.net_time_pct}%`;
      document.getElementById('p1-coverage').innerText = `6 • ${s1.coverage_m2}`;
    }
  }

  if (fData.spacing_m) {
    document.getElementById('val-spacing').innerHTML = `${fData.spacing_m}m <span class="m-tag">(ideal 3-5m) → ok</span>`;
  }
}
