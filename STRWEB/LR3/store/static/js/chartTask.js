// chartTask.js — computes series and draws Chart.js chart for the LR3 task
(function(){
  'use strict';

  // Target function and its series for Variant 1 from the assignment:
  // F(x) = ln((x+1)/(x-1))
  // Series for |x|>1: F(x) = 2 * sum_{k=0..infty} 1/((2k+1) * x^{2k+1})

  function exactF(x){
    // avoid singularities
    if (x === 1 || x === -1) return NaN;
    return Math.log((x + 1) / (x - 1));
  }

  function seriesApprox(x, N){
    // compute S_N(x) = 2 * sum_{k=0..N-1} 1/((2k+1) * x^{2k+1})
    // for small |x| this grows quickly; we compute anyway but mark as unreliable when |x|<=1
    let s = 0;
    for (let k = 0; k < N; k++){
      const denom = (2*k + 1) * Math.pow(x, 2*k + 1);
      if (denom === 0) { s = NaN; break; }
      s += 1 / denom;
    }
    return 2 * s;
  }

  // generate points between xMin and xMax (inclusive) with count points
  function generatePoints(xMin, xMax, count){
    const arr = [];
    const step = (xMax - xMin) / Math.max(1, count - 1);
    for (let i = 0; i < count; i++){
      arr.push(xMin + step * i);
    }
    return arr;
  }

  // create / update chart
  let chart = null;

  function drawChart(opts){
    const n = Number(document.getElementById('termsN').value) || 5;
    const xMin = Number(document.getElementById('xMin').value) || 1.2;
    const xMax = Number(document.getElementById('xMax').value) || 10;

    const xs = generatePoints(xMin, xMax, 200);
    const exactData = [];
    const seriesData = [];
    const labels = [];

    xs.forEach((x) => {
      labels.push(x.toFixed(2));
      const ex = exactF(x);
      const sr = seriesApprox(x, n);
      exactData.push(isFinite(ex) ? ex : null);
      seriesData.push(isFinite(sr) ? sr : null);
    });

    const ctx = document.getElementById('chartCanvas').getContext('2d');

    const data = {
      labels: labels,
      datasets: [
        {
          label: `F(x) = ln((x+1)/(x-1))`,
          data: exactData,
          borderColor: 'rgba(54, 162, 235, 1)',
          backgroundColor: 'rgba(54, 162, 235, 0.1)',
          pointRadius: 0,
          tension: 0.2,
        },
        {
          label: `Ряд, N=${n}`,
          data: seriesData,
          borderColor: 'rgba(255, 159, 64, 1)',
          backgroundColor: 'rgba(255, 159, 64, 0.08)',
          pointRadius: 0,
          tension: 0.2,
        }
      ]
    };

    const cfg = {
      type: 'line',
      data: data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          duration: 700,
          easing: 'easeOutCubic'
        },
        plugins: {
          legend: { position: 'top' },
          title: { display: true, text: 'График функции и частичной суммы ряда' }
        },
        scales: {
          x: {
            display: true,
            title: { display: true, text: 'x' }
          },
          y: {
            display: true,
            title: { display: true, text: 'F(x)' }
          }
        }
      }
    };

    if (chart) {
      // update dataset values and title
      chart.data = data;
      chart.options.plugins.title.text = `График функции и частичной суммы ряда (N=${n})`;
      chart.update();
    } else {
      chart = new Chart(ctx, cfg);
    }
  }

  // download current chart as PNG
  function downloadChart(){
    if (!chart) return;
    const url = chart.toBase64Image();
    const a = document.createElement('a');
    a.href = url;
    a.download = 'chart_lr3.png';
    document.body.appendChild(a);
    a.click();
    a.remove();
  }

  // helper: load script with fallback URLs
  function ensureChartJs(callback) {
    if (window.Chart) { callback(); return; }
    const urls = [
      'https://cdn.jsdelivr.net/npm/chart.js',
      'https://unpkg.com/chart.js/dist/chart.umd.min.js',
      'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.3.0/chart.min.js'
    ];
    let idx = 0;

    function tryLoadNext() {
      if (window.Chart) { callback(); return; }
      if (idx >= urls.length) {
        console.error('Failed to load Chart.js from all CDNs');
        alert('Не удалось загрузить Chart.js. Проверьте подключение к Интернету или разрешения в браузере.');
        return;
      }
      const url = urls[idx++];
      const s = document.createElement('script');
      s.src = url;
      s.crossOrigin = 'anonymous';
      s.onload = function() {
        // give the browser a tick to set window.Chart
        setTimeout(() => {
          if (window.Chart) callback();
          else tryLoadNext();
        }, 50);
      };
      s.onerror = function() {
        console.warn('Chart.js load failed from', url);
        tryLoadNext();
      };
      document.head.appendChild(s);
    }

    tryLoadNext();
  }

  // wire UI after Chart.js is available
  document.addEventListener('DOMContentLoaded', () => {
    ensureChartJs(() => {
      const redrawBtn = document.getElementById('redrawBtn');
      const downloadBtn = document.getElementById('downloadBtn');
      if (redrawBtn) redrawBtn.addEventListener('click', () => drawChart());
      if (downloadBtn) downloadBtn.addEventListener('click', downloadChart);
      // initial draw
      try {
        drawChart();
      } catch (err) {
        console.error('Failed to draw chart', err);
      }
    });
  });

})();
