// ── Extracted from index.html — single source for both index.html and queue.html ──
// Edit scenes here; both editor tools load this file via <script src="scenes.js">.

const LETTERS_HE = ['א','ב','ג','ד'];
const LETTERS_EN = ['A','B','C','D'];

// ── Scenes SVG ─────────────────────────────────────────────────────────────
const SCENES = {
'תדלוק ואש': `
  <rect width="360" height="420" fill="#0a1428"/>
  <rect x="0" y="246" width="360" height="174" fill="#1a5276"/>
  <g opacity="0.12"><path d="M0 292 Q90 284 180 292 Q270 300 360 292" fill="none" stroke="white" stroke-width="1.5"/><path d="M0 344 Q90 336 180 344 Q270 352 360 344" fill="none" stroke="white" stroke-width="1.5"/></g>
  <!-- fuel dock, running off the left edge and standing in the water -->
  <rect x="0" y="242" width="132" height="12" rx="2" fill="#8b7355"/>
  <rect x="16" y="254" width="11" height="86" fill="#6b5a45"/><rect x="100" y="254" width="11" height="86" fill="#6b5a45"/>
  <rect x="16" y="276" width="95" height="5" fill="#6b5a45" opacity="0.8"/>
  <!-- extinguisher within reach -->
  <g transform="translate(34,216)"><rect x="-9" y="0" width="18" height="26" rx="4" fill="#c0392b" stroke="#7b241c" stroke-width="1.5"/><rect x="-3" y="-6" width="6" height="7" fill="#7b241c"/><path d="M3 -3 L13 -8" stroke="#7b241c" stroke-width="2.5"/></g>
  <text x="62" y="200" text-anchor="middle" fill="#2ecc71" font-size="11" font-family="Heebo,sans-serif" font-weight="700">מטף בהישג יד</text>
  <text x="150" y="128" text-anchor="middle" fill="#7eb8f7" font-size="11" font-family="Heebo,sans-serif">אוורר את תא המנוע לפני התנעה</text>
  <!-- no naked flame / no smoking -->
  <g transform="translate(150,168)">
    <circle r="25" fill="none" stroke="#e74c3c" stroke-width="5"/>
    <rect x="-13" y="-4" width="21" height="8" rx="2" fill="#fff"/><rect x="9" y="-4" width="5" height="8" rx="2" fill="#e67e22"/>
    <line x1="-18" y1="18" x2="18" y2="-18" stroke="#e74c3c" stroke-width="5" stroke-linecap="round"/>
  </g>
  <text x="258" y="164" text-anchor="middle" fill="#e74c3c" font-size="12" font-family="Heebo,sans-serif" font-weight="700">אסור עישון</text>
  <text x="258" y="181" text-anchor="middle" fill="#e74c3c" font-size="12" font-family="Heebo,sans-serif" font-weight="700">ואש גלויה</text>
  <!-- hose from the dock to the filler -->
  <path d="M126 250 Q182 250 232 268" fill="none" stroke="#2c3e50" stroke-width="5" stroke-linecap="round"/>
  <rect x="228" y="264" width="12" height="8" rx="2" fill="#95a5a6"/>
  <!-- the craft alongside -->
  ${sideJetSki(248, 282, '#f1c40f', '#c8a000', 0.95)}
  <text x="250" y="312" text-anchor="middle" fill="#fff" font-size="12" font-family="Heebo,sans-serif" font-weight="700">כבה מנוע לפני תדלוק</text>
`,
'משולש האש': `
  <rect width="360" height="420" fill="#0a1020"/>
  <circle cx="46" cy="130" r="1" fill="white" opacity=".35"/><circle cx="316" cy="140" r="1.2" fill="white" opacity=".3"/>
  <!-- glow behind the triangle -->
  <circle cx="180" cy="222" r="96" fill="#e74c3c" opacity="0.07"/>
  <circle cx="180" cy="222" r="64" fill="#f39c12" opacity="0.08"/>
  <!-- the triangle: heat / oxygen / fuel -->
  <path d="M180 145 L255 275 L105 275 Z" fill="none" stroke="#e74c3c" stroke-width="4" stroke-linejoin="round"/>
  <path d="M180 145 L105 275" fill="none" stroke="#e74c3c" stroke-width="5"/>
  <path d="M105 275 L255 275" fill="none" stroke="#f39c12" stroke-width="5"/>
  <path d="M180 145 L255 275" fill="none" stroke="#3498db" stroke-width="5"/>
  <!-- flame in the middle -->
  <path d="M180 196 Q196 216 190 234 Q186 246 180 250 Q174 246 170 234 Q164 216 180 196 Z" fill="#f39c12"/>
  <path d="M180 214 Q188 226 184 238 Q182 244 180 246 Q178 244 176 238 Q172 226 180 214 Z" fill="#ffe27a"/>
  <!-- side labels, kept outside the triangle -->
  <text x="80" y="200" text-anchor="middle" fill="#e74c3c" font-size="15" font-family="Heebo,sans-serif" font-weight="900">חום</text>
  <text x="286" y="196" text-anchor="middle" fill="#3498db" font-size="15" font-family="Heebo,sans-serif" font-weight="900">חמצן</text>
  <text x="180" y="297" text-anchor="middle" fill="#f39c12" font-size="15" font-family="Heebo,sans-serif" font-weight="900">חומר בעירה</text>
  <!-- the extinguisher cuts the oxygen side -->
  <g transform="translate(217,210) rotate(60)">
    <line x1="-21" y1="0" x2="21" y2="0" stroke="#0a1020" stroke-width="9" stroke-linecap="round"/>
    <line x1="-21" y1="0" x2="21" y2="0" stroke="#2ecc71" stroke-width="4.5" stroke-linecap="round"/>
  </g>
  <text x="286" y="216" text-anchor="middle" fill="#2ecc71" font-size="11" font-family="Heebo,sans-serif" font-weight="700">המטף מנתק</text>
  <text x="180" y="134" text-anchor="middle" fill="#7eb8f7" font-size="11" font-family="Heebo,sans-serif" opacity="0.9">די לנתק צלע אחת</text>
`,
'אזורי שיט': `
  <rect width="360" height="420" fill="#1a5276"/>
  <g opacity="0.12"><path d="M0 70 Q90 60 180 70 Q270 80 360 70" fill="none" stroke="white" stroke-width="1.5"/><path d="M0 170 Q90 160 180 170 Q270 180 360 170" fill="none" stroke="white" stroke-width="1.5"/><path d="M0 270 Q90 260 180 270 Q270 280 360 270" fill="none" stroke="white" stroke-width="1.5"/><path d="M0 370 Q90 360 180 370 Q270 380 360 370" fill="none" stroke="white" stroke-width="1.5"/></g>
  <!-- shore on the left: sand + waterline -->
  <path d="M0 0 L64 0 Q72 60 66 120 Q60 200 70 280 Q76 360 64 420 L0 420 Z" fill="#d9c08a"/>
  <path d="M64 0 Q72 60 66 120 Q60 200 70 280 Q76 360 64 420" fill="none" stroke="#f2e2b8" stroke-width="3" opacity="0.85"/>
  <!-- 300 m band. Everything readable is kept inside y 120-305, the band that
       actually survives the preserveAspectRatio="slice" crop in the reel. -->
  <rect x="68" y="0" width="112" height="420" fill="white" opacity="0.09"/>
  <line x1="180" y1="0" x2="180" y2="420" stroke="#7eb8f7" stroke-width="2" stroke-dasharray="7,5" opacity="0.8"/>
  <text x="243" y="300" text-anchor="middle" fill="#7eb8f7" font-size="12" font-family="Heebo,sans-serif" font-weight="700">300 מ' מקו החוף</text>
  <!-- declared bathing beach -->
  <rect x="66" y="132" width="26" height="62" fill="#e74c3c" opacity="0.32"/>
  <g stroke="#e74c3c" stroke-width="2.5"><line x1="60" y1="132" x2="96" y2="132"/><line x1="60" y1="194" x2="96" y2="194"/></g>
  <g fill="#e74c3c"><rect x="46" y="126" width="2.5" height="24"/><path d="M48.5 126 L63 132 L48.5 138 Z"/><rect x="46" y="188" width="2.5" height="24"/><path d="M48.5 188 L63 194 L48.5 200 Z"/></g>
  <line x1="100" y1="158" x2="192" y2="158" stroke="#e74c3c" stroke-width="1.5" stroke-dasharray="4,3" opacity="0.7"/>
  <text x="262" y="154" text-anchor="middle" fill="#e74c3c" font-size="12" font-family="Heebo,sans-serif" font-weight="700">חוף רחצה מוכרז</text>
  <text x="262" y="170" text-anchor="middle" fill="#e74c3c" font-size="10" font-family="Heebo,sans-serif" opacity="0.85">אסור בהשקה</text>
  <!-- launch point on a non-bathing beach + perpendicular exit -->
  <circle cx="72" cy="252" r="7" fill="#f1c40f" stroke="#0c1a3a" stroke-width="2"/>
  <text x="122" y="286" text-anchor="middle" fill="#f1c40f" font-size="11" font-family="Heebo,sans-serif" font-weight="700">נקודת השקה</text>
  <path d="M88 252 L300 252" stroke="#2ecc71" stroke-width="2.5" stroke-dasharray="8,5" marker-end="url(#arrZ)"/>
  <defs><marker id="arrZ" markerWidth="9" markerHeight="9" refX="7" refY="3.2" orient="auto"><path d="M0,0 L0,6.4 L9,3.2 z" fill="#2ecc71"/></marker></defs>
  <path d="M98 232 L122 232 M98 232 L98 246" stroke="#2ecc71" stroke-width="2" opacity="0.9"/>
  <text x="136" y="228" text-anchor="middle" fill="#2ecc71" font-size="10" font-family="Heebo,sans-serif" font-weight="700">90°</text>
  <text x="248" y="230" text-anchor="middle" fill="#fff" font-size="12" font-family="Heebo,sans-serif" font-weight="700">עד 5 קשרים</text>
  <g>
    <g transform="translate(112,252) rotate(90)"><ellipse cx="0" cy="0" rx="11" ry="24" fill="#f1c40f" stroke="#c8a000" stroke-width="1.5"/><ellipse cx="0" cy="-8" rx="6" ry="9" fill="#ffe27a"/><circle cx="0" cy="-8" r="2.5" fill="#5a4a00"/></g>
    <animateTransform attributeName="transform" type="translate" values="0,0;168,0;168,0" dur="5s" repeatCount="indefinite" keyTimes="0;0.7;1" calcMode="spline" keySplines="0.35 0 0.25 1;0 0 1 1"/>
  </g>
`,
'כניסה לנמל': `
  <rect width="360" height="420" fill="#1a5276"/>
  <g opacity="0.12"><path d="M0 60 Q90 50 180 60 Q270 70 360 60" fill="none" stroke="white" stroke-width="1.5"/><path d="M0 140 Q90 130 180 140 Q270 150 360 140" fill="none" stroke="white" stroke-width="1.5"/><path d="M0 220 Q90 210 180 220 Q270 230 360 220" fill="none" stroke="white" stroke-width="1.5"/><path d="M0 300 Q90 290 180 300 Q270 310 360 300" fill="none" stroke="white" stroke-width="1.5"/></g>
  <rect x="40" y="0" width="22" height="240" rx="6" fill="#2c5282"/><rect x="298" y="0" width="22" height="240" rx="6" fill="#2c5282"/>
  <rect x="0" y="0" width="40" height="250" fill="#1a3a1a" opacity="0.6"/><rect x="320" y="0" width="40" height="250" fill="#1a3a1a" opacity="0.6"/>
  <circle cx="319" cy="248" r="16" fill="#1a4a2a"/><circle cx="319" cy="248" r="13" fill="#27ae60"><animate attributeName="opacity" values="1;0.1;1" dur="1.4s" repeatCount="indefinite"/></circle>
  <circle cx="319" cy="248" r="22" fill="#2ecc71" opacity="0"><animate attributeName="opacity" values="0;0.35;0" dur="1.4s" repeatCount="indefinite"/></circle>
  <text x="319" y="274" text-anchor="middle" fill="#2ecc71" font-size="11" font-family="Heebo,sans-serif" font-weight="700">ירוק</text>
  <text x="319" y="287" text-anchor="middle" fill="#7eb8f7" font-size="9" font-family="Arial">Starboard</text>
  <circle cx="41" cy="248" r="16" fill="#4a1a1a"/><circle cx="41" cy="248" r="13" fill="#c0392b"><animate attributeName="opacity" values="1;0.1;1" dur="1.4s" repeatCount="indefinite" begin="0.7s"/></circle>
  <circle cx="41" cy="248" r="22" fill="#e74c3c" opacity="0"><animate attributeName="opacity" values="0;0.35;0" dur="1.4s" repeatCount="indefinite" begin="0.7s"/></circle>
  <text x="41" y="274" text-anchor="middle" fill="#e74c3c" font-size="11" font-family="Heebo,sans-serif" font-weight="700">אדום</text>
  <text x="41" y="287" text-anchor="middle" fill="#7eb8f7" font-size="9" font-family="Arial">Port</text>
  <text x="180" y="228" text-anchor="middle" fill="#7eb8f7" font-size="10" font-family="Heebo,sans-serif" opacity="0.8">— כניסה למרינה —</text>
  <g><ellipse cx="180" cy="390" rx="18" ry="36" fill="#e8e8e8" stroke="#aaa" stroke-width="1"/><ellipse cx="180" cy="370" rx="10" ry="13" fill="#ccc"/><circle cx="180" cy="370" r="3" fill="#666"/>
  <animateTransform attributeName="transform" type="translate" values="0,0;0,-155;0,-155" dur="5s" repeatCount="indefinite" keyTimes="0;0.65;1" calcMode="spline" keySplines="0.4 0 0.2 1;0 0 1 1"/></g>
`,
'אורות ניווט': `
  <rect width="360" height="420" fill="#050d1a"/>
  <circle cx="50" cy="40" r="1.5" fill="white" opacity="0.8"/><circle cx="120" cy="20" r="1" fill="white" opacity="0.7"/><circle cx="200" cy="50" r="1.5" fill="white" opacity="0.9"/><circle cx="280" cy="30" r="1" fill="white" opacity="0.6"/><circle cx="320" cy="70" r="2" fill="white" opacity="0.8"/>
  <g transform="translate(180,230)">
    <ellipse cx="0" cy="0" rx="24" ry="50" fill="#1a2a3a" stroke="#2a4a6a" stroke-width="1.5"/>
    <ellipse cx="0" cy="-15" rx="14" ry="18" fill="#1a2a3a" stroke="#2a4a6a" stroke-width="1"/>
    <circle cx="22" cy="-5" r="7" fill="#27ae60"><animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/></circle>
    <circle cx="22" cy="-5" r="14" fill="#2ecc71" opacity="0"><animate attributeName="opacity" values="0;0.4;0" dur="2s" repeatCount="indefinite"/></circle>
    <circle cx="-22" cy="-5" r="7" fill="#c0392b"><animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite" begin="1s"/></circle>
    <circle cx="-22" cy="-5" r="14" fill="#e74c3c" opacity="0"><animate attributeName="opacity" values="0;0.4;0" dur="2s" repeatCount="indefinite" begin="1s"/></circle>
    <line x1="0" y1="-50" x2="0" y2="10" stroke="#555" stroke-width="2"/>
    <circle cx="0" cy="-55" r="7" fill="#fffacd"><animate attributeName="opacity" values="1;0.6;1" dur="3s" repeatCount="indefinite"/></circle>
  </g>
  <text x="205" y="225" fill="#2ecc71" font-size="10" font-family="Arial">Green/Starboard</text>
  <text x="100" y="225" fill="#e74c3c" font-size="10" font-family="Arial">Red/Port</text>
  <text x="180" y="380" text-anchor="middle" fill="#7eb8f7" font-size="11" font-family="Heebo,sans-serif">כלי שייט בלילה — זהה את האורות</text>
`,
'זכות מעבר': `
  <rect width="360" height="420" fill="#1a5276"/>
  <g opacity="0.12"><path d="M0 80 Q90 70 180 80 Q270 90 360 80" fill="none" stroke="white" stroke-width="1.5"/><path d="M0 200 Q90 190 180 200 Q270 210 360 200" fill="none" stroke="white" stroke-width="1.5"/><path d="M0 320 Q90 310 180 320 Q270 330 360 320" fill="none" stroke="white" stroke-width="1.5"/></g>
  <g transform="translate(70,210) rotate(90)"><ellipse cx="0" cy="0" rx="16" ry="34" fill="#e8d8b0" stroke="#999" stroke-width="1"/><ellipse cx="0" cy="-12" rx="9" ry="12" fill="#d4c090"/><circle cx="0" cy="-12" r="3" fill="#666"/></g>
  <text x="70" y="258" text-anchor="middle" fill="#fff" font-size="16" font-family="Heebo,sans-serif" font-weight="900">A</text>
  <path d="M95 210 L165 210" stroke="#7eb8f7" stroke-width="2" stroke-dasharray="6,3" marker-end="url(#arr)"/>
  <g transform="translate(250,100)"><ellipse cx="0" cy="0" rx="16" ry="34" fill="#e8e8e8" stroke="#999" stroke-width="1"/><ellipse cx="0" cy="-12" rx="9" ry="12" fill="#ccc"/><circle cx="0" cy="-12" r="3" fill="#666"/></g>
  <text x="250" y="148" text-anchor="middle" fill="#fff" font-size="16" font-family="Heebo,sans-serif" font-weight="900">B</text>
  <path d="M250 138 L250 200" stroke="#7eb8f7" stroke-width="2" stroke-dasharray="6,3" marker-end="url(#arr)"/>
  <defs><marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#7eb8f7"/></marker></defs>
  <text x="180" y="210" text-anchor="middle" fill="#ff0" font-size="32">⚠</text>
  <text x="180" y="360" text-anchor="middle" fill="#7eb8f7" font-size="11" font-family="Heebo,sans-serif">מי נותן זכות מעבר?</text>
`,
'אותות מצוקה': `
  <rect width="360" height="420" fill="#1a3a5c"/>
  <g opacity="0.12"><path d="M0 100 Q90 90 180 100 Q270 110 360 100" fill="none" stroke="white" stroke-width="1.5"/><path d="M0 250 Q90 240 180 250 Q270 260 360 250" fill="none" stroke="white" stroke-width="1.5"/></g>
  <g transform="translate(180,260) rotate(12)">
    <ellipse cx="0" cy="0" rx="40" ry="18" fill="#8b4513" stroke="#6b3410" stroke-width="2"/>
    <rect x="-15" y="-30" width="4" height="32" fill="#555"/>
    <g transform="translate(20,-40)">
      <line x1="0" y1="0" x2="0" y2="-60" stroke="#e74c3c" stroke-width="3" opacity="0"><animate attributeName="opacity" values="0;1;0.8;0" dur="1.5s" repeatCount="indefinite"/></line>
      <circle cx="0" cy="-60" r="10" fill="#ff4500" opacity="0"><animate attributeName="opacity" values="0;1;0.8;0" dur="1.5s" repeatCount="indefinite"/></circle>
    </g>
  </g>
  <text x="180" y="380" text-anchor="middle" fill="#e74c3c" font-size="16" font-family="Heebo,sans-serif" font-weight="900">MAYDAY ⚠</text>
`,
'עגינה': `
  <rect width="360" height="420" fill="#1a5276"/>
  <g opacity="0.12"><path d="M0 80 Q90 70 180 80 Q270 90 360 80" fill="none" stroke="white" stroke-width="1.5"/><path d="M0 200 Q90 190 180 200 Q270 210 360 200" fill="none" stroke="white" stroke-width="1.5"/><path d="M0 320 Q90 310 180 320 Q270 330 360 320" fill="none" stroke="white" stroke-width="1.5"/></g>
  <rect x="0" y="380" width="360" height="50" fill="#8b7355" opacity="0.6"/>
  <line x1="180" y1="210" x2="180" y2="385" stroke="#aaa" stroke-width="2" stroke-dasharray="8,4"/>
  <g transform="translate(180,390)"><circle cx="0" cy="-5" r="8" fill="none" stroke="#aaa" stroke-width="2.5"/><line x1="0" y1="-13" x2="0" y2="8" stroke="#aaa" stroke-width="2.5"/><line x1="-10" y1="8" x2="10" y2="8" stroke="#aaa" stroke-width="2.5"/></g>
  <g transform="translate(180,190)"><ellipse cx="0" cy="0" rx="20" ry="42" fill="#e8e8e8" stroke="#aaa" stroke-width="1"/><ellipse cx="0" cy="-14" rx="11" ry="15" fill="#ccc"/><circle cx="0" cy="-14" r="3" fill="#666"/><circle cx="0" cy="-52" r="7" fill="white" stroke="#888" stroke-width="1"/></g>
  <text x="230" y="310" fill="#7eb8f7" font-size="11" font-family="Arial">depth: 5m</text>
  <text x="230" y="360" fill="#7eb8f7" font-size="11" font-family="Arial">chain = ?</text>
`,
'זכות_מעבר_מפרש': `
  <rect width="360" height="420" fill="#0d3d57"/>
  <g opacity="0.1">
    <path d="M0 90 Q90 80 180 90 Q270 100 360 90" fill="none" stroke="white" stroke-width="1.5"/>
    <path d="M0 175 Q90 165 180 175 Q270 185 360 175" fill="none" stroke="white" stroke-width="1.5"/>
    <path d="M0 260 Q90 250 180 260 Q270 270 360 260" fill="none" stroke="white" stroke-width="1.5"/>
    <path d="M0 345 Q90 335 180 345 Q270 355 360 345" fill="none" stroke="white" stroke-width="1.5"/>
  </g>
  <defs>
    <marker id="ga" markerWidth="10" markerHeight="8" refX="7" refY="4" orient="auto">
      <path d="M0,0 L0,8 L10,4 z" fill="#e67e22"/>
    </marker>
  </defs>
  <text x="180" y="22" text-anchor="middle" fill="#7eb8f7" font-size="12" font-family="Heebo,sans-serif" font-weight="700">💨 כיוון הרוח</text>
  <line x1="75" y1="30" x2="75" y2="56" stroke="#7eb8f7" stroke-width="2.5"/>
  <polygon points="75,61 69,51 81,51" fill="#7eb8f7"/>
  <line x1="180" y1="30" x2="180" y2="56" stroke="#7eb8f7" stroke-width="2.5"/>
  <polygon points="180,61 174,51 186,51" fill="#7eb8f7"/>
  <line x1="285" y1="30" x2="285" y2="56" stroke="#7eb8f7" stroke-width="2.5"/>
  <polygon points="285,61 279,51 291,51" fill="#7eb8f7"/>
  <line x1="135" y1="215" x2="232" y2="215" stroke="#7eb8f7" stroke-width="1" stroke-dasharray="5,4" opacity="0.35"/>
  <!-- PORT TACK (left, give-way) heading east — wind from north = from port (left) side -->
  <g transform="translate(90,215)">
    <g>
      <animateTransform attributeName="transform" type="rotate"
        values="0;0;0;55;55;0"
        keyTimes="0;0.18;0.42;0.62;0.82;1"
        dur="7s" calcMode="linear" repeatCount="indefinite"/>
      <ellipse cx="0" cy="0" rx="38" ry="13" fill="#f5e8c8" stroke="#e67e22" stroke-width="2"/>
      <polygon points="40,-9 40,9 52,0" fill="#d4b870"/>
      <line x1="-38" y1="-11" x2="-38" y2="11" stroke="#c9a050" stroke-width="2"/>
      <circle cx="5" cy="0" r="4" fill="#444"/>
      <line x1="5" y1="-13" x2="5" y2="13" stroke="#777" stroke-width="1.5"/>
      <path d="M5,0 L42,-11 L36,7" fill="rgba(255,248,210,0.6)" stroke="#d4b870" stroke-width="0.8"/>
      <line x1="5" y1="0" stroke="#777" stroke-width="2.5">
        <animate attributeName="x2" values="-20;-20;-20;-20;-20;-20" keyTimes="0;0.18;0.5;0.6;0.82;1" dur="7s" repeatCount="indefinite"/>
        <animate attributeName="y2" values="26;26;26;-26;-26;26" keyTimes="0;0.18;0.5;0.6;0.82;1" dur="7s" repeatCount="indefinite"/>
      </line>
      <path fill="rgba(245,228,150,0.8)" stroke="#d4b870" stroke-width="1.2">
        <animate attributeName="d" values="M5,0 L-20,26 L-30,5;M5,0 L-20,26 L-30,5;M5,0 L-20,26 L-30,5;M5,0 L-20,-26 L-30,-5;M5,0 L-20,-26 L-30,-5;M5,0 L-20,26 L-30,5" keyTimes="0;0.18;0.5;0.6;0.82;1" dur="7s" repeatCount="indefinite"/>
      </path>
    </g>
    <text x="0" y="-24" text-anchor="middle" fill="#ff9944" font-size="10" font-family="Heebo,sans-serif" font-weight="900">Port Tack — מפנה! ↻</text>
  </g>
  <path d="M102,177 Q68,144 80,110" fill="none" stroke="#e67e22" stroke-width="2.5" stroke-dasharray="5,3" marker-end="url(#ga)">
    <animate attributeName="opacity" values="0;0;0;1;1;0" keyTimes="0;0.38;0.42;0.58;0.8;1" dur="7s" repeatCount="indefinite"/>
  </path>
  <text x="60" y="106" fill="#e67e22" font-size="9" font-family="Heebo,sans-serif" font-weight="700">
    <animate attributeName="opacity" values="0;0;0;1;1;0" keyTimes="0;0.38;0.42;0.58;0.8;1" dur="7s" repeatCount="indefinite"/>גייב!
  </text>
  <text x="182" y="222" text-anchor="middle" fill="#ffcc00" font-size="30">
    <animate attributeName="opacity" values="0.9;0.9;0.9;0;0;0.9" keyTimes="0;0.1;0.38;0.48;0.82;1" dur="7s" repeatCount="indefinite"/>⚠
  </text>
  <!-- STARBOARD TACK (right, stand-on) heading west — wind from north = from starboard (right) side -->
  <g transform="translate(270,215)">
    <ellipse cx="0" cy="0" rx="38" ry="13" fill="#e8f5e2" stroke="#2ecc71" stroke-width="2"/>
    <polygon points="-40,-9 -40,9 -52,0" fill="#a8e098"/>
    <line x1="38" y1="-11" x2="38" y2="11" stroke="#88d078" stroke-width="2"/>
    <circle cx="-5" cy="0" r="4" fill="#444"/>
    <line x1="-5" y1="-13" x2="-5" y2="13" stroke="#777" stroke-width="1.5"/>
    <path d="M-5,0 L-42,-11 L-36,7" fill="rgba(200,240,180,0.6)" stroke="#88d078" stroke-width="0.8"/>
    <line x1="-5" y1="0" x2="18" y2="26" stroke="#777" stroke-width="2.5"/>
    <path d="M-5,0 L18,26 L28,4" fill="rgba(180,240,170,0.8)" stroke="#88d078" stroke-width="1.2"/>
    <text x="0" y="-24" text-anchor="middle" fill="#2ecc71" font-size="10" font-family="Heebo,sans-serif" font-weight="900">Starboard Tack — עדיפות ✓</text>
  </g>
  <text x="180" y="295" text-anchor="middle" fill="#7eb8f7" font-size="11" font-family="Heebo,sans-serif" font-weight="700">Port → חייב לפנות (גייב דרך הירכתיים)</text>
  <text x="180" y="310" text-anchor="middle" fill="#7eb8f7" font-size="9" font-family="Arial" opacity="0.75">COLREGS Rule 12: Port tack vessel gives way</text>
`
};
// ── Additional Scenes ────────────────────────────────────────────────────────
Object.assign(SCENES, {

'ניווט': `
  <rect width="360" height="420" fill="#0a1a30"/>
  <rect x="20" y="20" width="320" height="230" rx="8" fill="#0d2040" stroke="#2a4a6a" stroke-width="1.5"/>
  <line x1="20" y1="135" x2="340" y2="135" stroke="#1e3a5a" stroke-width="1"/>
  <line x1="180" y1="20" x2="180" y2="250" stroke="#1e3a5a" stroke-width="1"/>
  <text x="180" y="40" text-anchor="middle" fill="#4a8ac0" font-size="9" font-family="Arial">90°N</text>
  <text x="180" y="248" text-anchor="middle" fill="#4a8ac0" font-size="9" font-family="Arial">90°S</text>
  <text x="25" y="138" fill="#4a8ac0" font-size="9" font-family="Arial">180°W</text>
  <text x="310" y="138" fill="#4a8ac0" font-size="9" font-family="Arial">180°E</text>
  <path d="M20,100 Q90,90 180,100 Q270,110 340,100" fill="none" stroke="#2e6ea6" stroke-width="1.5"/>
  <path d="M20,135 Q340,135 340,135" fill="none" stroke="#3a80b8" stroke-width="2"/>
  <path d="M20,170 Q90,180 180,170 Q270,160 340,170" fill="none" stroke="#2e6ea6" stroke-width="1.5"/>
  <path d="M20,55 Q90,48 180,55 Q270,62 340,55" fill="none" stroke="#1e5080" stroke-width="1"/>
  <path d="M20,215 Q90,222 180,215 Q270,208 340,215" fill="none" stroke="#1e5080" stroke-width="1"/>
  <line x1="110" y1="20" x2="110" y2="250" stroke="#1a3a58" stroke-width="0.8"/>
  <line x1="250" y1="20" x2="250" y2="250" stroke="#1a3a58" stroke-width="0.8"/>
  <circle cx="180" cy="135" r="5" fill="#4a90d9"><animate attributeName="r" values="5;8;5" dur="2s" repeatCount="indefinite"/></circle>
  <circle cx="180" cy="135" r="12" fill="none" stroke="#4a90d9" opacity="0.5"><animate attributeName="r" values="8;20;8" dur="2s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.5;0;0.5" dur="2s" repeatCount="indefinite"/></circle>
  <path d="M180,135 L230,85" stroke="#7eb8f7" stroke-width="2" stroke-dasharray="4,3"/>
  <text x="235" y="82" fill="#7eb8f7" font-size="11" font-family="Arial" font-weight="700">B</text>
  <text x="162" y="152" fill="#2ecc71" font-size="11" font-family="Arial" font-weight="700">A</text>
  <g transform="translate(20,265)">
    <text x="0" y="15" fill="#7eb8f7" font-size="11" font-family="Heebo,sans-serif" font-weight="700">קורס: </text>
    <text x="52" y="15" fill="#fff" font-size="11" font-family="Arial" font-weight="700">045°M</text>
    <text x="120" y="15" fill="#7eb8f7" font-size="11" font-family="Heebo,sans-serif" font-weight="700">מהירות: </text>
    <text x="178" y="15" fill="#fff" font-size="11" font-family="Arial" font-weight="700">6.2 kn</text>
  </g>
  <g transform="translate(20,290)">
    <text x="0" y="15" fill="#7eb8f7" font-size="11" font-family="Heebo,sans-serif" font-weight="700">N </text>
    <text x="14" y="15" fill="#fff" font-size="11" font-family="Arial">32°04.5'</text>
    <text x="105" y="15" fill="#7eb8f7" font-size="11" font-family="Heebo,sans-serif" font-weight="700">E </text>
    <text x="118" y="15" fill="#fff" font-size="11" font-family="Arial">34°46.2'</text>
  </g>
  <text x="180" y="360" text-anchor="middle" fill="#4a8ac0" font-size="10" font-family="Heebo,sans-serif">ניווט על מפת מרקטור</text>
`,

'מצפן': `
  <rect width="360" height="420" fill="#080f1e"/>
  <circle cx="180" cy="180" r="130" fill="#0c1828" stroke="#1e3a5a" stroke-width="2"/>
  <circle cx="180" cy="180" r="120" fill="none" stroke="#1a3050" stroke-width="1"/>
  <circle cx="180" cy="180" r="100" fill="none" stroke="#162840" stroke-width="0.5"/>
  ${[0,30,60,90,120,150,180,210,240,270,300,330].map(d=>{
    const r=d%90===0?1.8:0.8, l=d%90===0?18:10, col=d%90===0?'#4a8ac0':'#2a5a7a';
    const rd=d*Math.PI/180, x1=180+108*Math.sin(rd), y1=180-108*Math.cos(rd), x2=180+(108-l)*Math.sin(rd), y2=180-(108-l)*Math.cos(rd);
    return `<line x1="${x1.toFixed(1)}" y1="${y1.toFixed(1)}" x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}" stroke="${col}" stroke-width="${r}"/>`;
  }).join('')}
  <text x="180" y="72" text-anchor="middle" fill="#e74c3c" font-size="14" font-family="Arial" font-weight="900">N</text>
  <text x="180" y="302" text-anchor="middle" fill="#7eb8f7" font-size="12" font-family="Arial" font-weight="700">S</text>
  <text x="295" y="186" text-anchor="middle" fill="#7eb8f7" font-size="12" font-family="Arial" font-weight="700">E</text>
  <text x="65" y="186" text-anchor="middle" fill="#7eb8f7" font-size="12" font-family="Arial" font-weight="700">W</text>
  <g>
    <animateTransform attributeName="transform" type="rotate" values="0 180 180;360 180 180" dur="8s" repeatCount="indefinite"/>
    <polygon points="180,90 175,180 185,180" fill="#e74c3c"/>
    <polygon points="180,270 175,180 185,180" fill="#7eb8f7"/>
  </g>
  <circle cx="180" cy="180" r="8" fill="#1e3a5a" stroke="#4a8ac0" stroke-width="1.5"/>
  <text x="180" y="380" text-anchor="middle" fill="#4a8ac0" font-size="10" font-family="Heebo,sans-serif">מצפן מגנטי — וריאציה ודוויאציה</text>
`,

'GPS': `
  <rect width="360" height="420" fill="#050d1a"/>
  ${[0,1,2,3,4,5].map(i=>{
    const cx=[80,200,310,140,260,50][i], cy=[60,40,100,160,180,140][i], r=[3,2,2.5,2,3,1.5][i];
    return `<circle cx="${cx}" cy="${cy}" r="${r}" fill="white" opacity="0.7"/>`;
  }).join('')}
  <circle cx="180" cy="210" r="140" fill="none" stroke="#1a3a5a" stroke-width="1" opacity="0.5"/>
  <circle cx="180" cy="210" r="100" fill="none" stroke="#1a4a6a" stroke-width="1" opacity="0.6"/>
  <circle cx="180" cy="210" r="60" fill="none" stroke="#1a5a7a" stroke-width="1" opacity="0.7"/>
  <circle cx="180" cy="210" r="8" fill="#4a90d9"/>
  <circle cx="180" cy="210" r="16" fill="none" stroke="#4a90d9" opacity="0.5"><animate attributeName="r" values="10;22;10" dur="2s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.6;0;0.6" dur="2s" repeatCount="indefinite"/></circle>
  ${[[60,55],[300,70],[250,165],[100,160]].map(([sx,sy],i)=>`
    <line x1="${sx}" y1="${sy}" x2="180" y2="210" stroke="#2a6a9a" stroke-width="1" stroke-dasharray="4,3" opacity="0.7">
      <animate attributeName="opacity" values="0.3;0.9;0.3" dur="${1.5+i*0.4}s" repeatCount="indefinite"/>
    </line>
    <rect x="${sx-10}" y="${sy-10}" width="20" height="14" rx="3" fill="#1a3a6a" stroke="#4a90d9" stroke-width="1"/>
    <text x="${sx}" y="${sy+2}" text-anchor="middle" fill="#7eb8f7" font-size="8" font-family="Arial">SAT</text>
  `).join('')}
  <rect x="50" y="320" width="260" height="50" rx="8" fill="#0d1e38" stroke="#2a4a7a" stroke-width="1"/>
  <text x="180" y="340" text-anchor="middle" fill="#7eb8f7" font-size="11" font-family="Heebo,sans-serif" font-weight="700">מיקום GPS</text>
  <text x="180" y="358" text-anchor="middle" fill="#fff" font-size="11" font-family="Arial">32°04.521'N  34°46.218'E</text>
`,

'קשר VHF': `
  <rect width="360" height="420" fill="#090f1a"/>
  <rect x="120" y="30" width="120" height="200" rx="12" fill="#0d1e38" stroke="#2a4a6a" stroke-width="2"/>
  <rect x="130" y="45" width="100" height="55" rx="5" fill="#050d1a" stroke="#1a3a5a" stroke-width="1"/>
  <text x="180" y="68" text-anchor="middle" fill="#2ecc71" font-size="11" font-family="Arial" font-weight="700">CH 16</text>
  <text x="180" y="85" text-anchor="middle" fill="#4a90d9" font-size="10" font-family="Arial">156.800 MHz</text>
  <line x1="180" y1="30" x2="180" y2="5" stroke="#7eb8f7" stroke-width="2"/>
  <line x1="180" y1="5" x2="200" y2="5" stroke="#7eb8f7" stroke-width="2"/>
  ${[0,1,2,3,4,5].map(i=>`
    <circle cx="${135+i*18}" cy="${118+Math.floor(i/3)*22}" r="7" fill="#0a1830" stroke="#2a4a6a" stroke-width="1"/>
    <text x="${135+i*18}" y="${122+Math.floor(i/3)*22}" text-anchor="middle" fill="#7eb8f7" font-size="8" font-family="Arial">${['1','2','3','4','5','6'][i]}</text>
  `).join('')}
  <circle cx="180" cy="195" r="14" fill="#0d3d2a" stroke="#2ecc71" stroke-width="2"/>
  <text x="180" y="199" text-anchor="middle" fill="#2ecc71" font-size="9" font-family="Arial" font-weight="700">PTT</text>
  ${[30,55,80,105,130,155].map((x,i)=>`
    <rect x="${x}" y="${280 - i*8}" width="14" height="${20+i*8}" rx="2" fill="#4a90d9" opacity="${0.3+i*0.12}">
      <animate attributeName="height" values="${20+i*8};${30+i*10};${20+i*8}" dur="${0.8+i*0.15}s" repeatCount="indefinite"/>
      <animate attributeName="y" values="${280-i*8};${270-i*10};${280-i*8}" dur="${0.8+i*0.15}s" repeatCount="indefinite"/>
    </rect>
  `).join('')}
  ${[195,220,245,270,295,320].map((x,i)=>`
    <rect x="${x}" y="${280 - (5-i)*6}" width="14" height="${20+(5-i)*6}" rx="2" fill="#4a90d9" opacity="${0.3+(5-i)*0.12}">
      <animate attributeName="height" values="${20+(5-i)*6};${30+(5-i)*8};${20+(5-i)*6}" dur="${0.9+(5-i)*0.13}s" repeatCount="indefinite"/>
      <animate attributeName="y" values="${280-(5-i)*6};${268-(5-i)*8};${280-(5-i)*6}" dur="${0.9+(5-i)*0.13}s" repeatCount="indefinite"/>
    </rect>
  `).join('')}
  <text x="180" y="360" text-anchor="middle" fill="#4a8ac0" font-size="10" font-family="Heebo,sans-serif">VHF Marine Radio — Channel 16</text>
`,

'מד עומק': `
  <rect width="360" height="420" fill="#061018"/>
  <rect x="20" y="20" width="320" height="260" rx="8" fill="#0a1828" stroke="#1a3a50" stroke-width="1.5"/>
  <line x1="20" y1="150" x2="340" y2="150" stroke="#2ecc71" stroke-width="1.5" opacity="0.3"/>
  <line x1="20" y1="200" x2="340" y2="200" stroke="#2ecc71" stroke-width="1" opacity="0.2"/>
  <line x1="20" y1="100" x2="340" y2="100" stroke="#2ecc71" stroke-width="1" opacity="0.2"/>
  <polyline points="20,100 60,110 100,95 140,130 160,140 190,155 220,148 260,160 300,145 340,158" fill="none" stroke="#2ecc71" stroke-width="2.5"/>
  <polygon points="20,100 60,110 100,95 140,130 160,140 190,155 220,148 260,160 300,145 340,158 340,280 20,280" fill="#0d3d1a" opacity="0.4"/>
  <line x1="190" y1="20" x2="190" y2="155" stroke="#4a90d9" stroke-width="1.5" stroke-dasharray="5,3">
    <animate attributeName="y2" values="20;155;155;20" dur="3s" repeatCount="indefinite" keyTimes="0;0.4;0.6;1"/>
  </line>
  <circle cx="190" cy="155" r="4" fill="#4a90d9"><animate attributeName="cy" values="20;155;155;20" dur="3s" repeatCount="indefinite" keyTimes="0;0.4;0.6;1"/></circle>
  <rect x="130" y="290" width="100" height="36" rx="6" fill="#0d1e38" stroke="#2ecc71" stroke-width="1.5"/>
  <text x="180" y="308" text-anchor="middle" fill="#2ecc71" font-size="11" font-family="Arial" font-weight="700">DEPTH</text>
  <text x="180" y="322" text-anchor="middle" fill="#fff" font-size="12" font-family="Arial" font-weight="900">12.4 m</text>
  <text x="180" y="385" text-anchor="middle" fill="#4a8ac0" font-size="10" font-family="Heebo,sans-serif">Echo Sounder — מד עומק</text>
`,

'הגה אוטומטי': `
  <rect width="360" height="420" fill="#080f1a"/>
  <circle cx="180" cy="175" r="120" fill="none" stroke="#1a3050" stroke-width="2"/>
  <circle cx="180" cy="175" r="115" fill="none" stroke="#0d2040" stroke-width="8"/>
  ${[0,30,60,90,120,150,180,210,240,270,300,330].map(d=>{
    const rd=d*Math.PI/180, x=180+108*Math.sin(rd), y=175-108*Math.cos(rd), x2=180+95*Math.sin(rd), y2=175-95*Math.cos(rd);
    return `<line x1="${x.toFixed(1)}" y1="${y.toFixed(1)}" x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}" stroke="${d===0?'#e74c3c':'#2a5a7a'}" stroke-width="${d%90===0?2:1}"/>`;
  }).join('')}
  <text x="180" y="70" text-anchor="middle" fill="#e74c3c" font-size="12" font-family="Arial" font-weight="900">N</text>
  <g>
    <animateTransform attributeName="transform" type="rotate" values="15 180 175;-15 180 175;15 180 175" dur="4s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1"/>
    <line x1="180" y1="175" x2="180" y2="85" stroke="#4a90d9" stroke-width="3" stroke-linecap="round"/>
    <polygon points="180,82 176,92 184,92" fill="#4a90d9"/>
  </g>
  <circle cx="180" cy="175" r="6" fill="#1e3a5a" stroke="#4a90d9" stroke-width="2"/>
  <rect x="60" y="315" width="240" height="40" rx="8" fill="#0d1e38" stroke="#4a90d9" stroke-width="1"/>
  <text x="180" y="331" text-anchor="middle" fill="#7eb8f7" font-size="10" font-family="Heebo,sans-serif">AUTO</text>
  <text x="180" y="348" text-anchor="middle" fill="#fff" font-size="13" font-family="Arial" font-weight="900">Course: 045°</text>
  <text x="180" y="400" text-anchor="middle" fill="#4a8ac0" font-size="10" font-family="Heebo,sans-serif">הגה אוטומטי — Autopilot</text>
`,

// Generic fallback for the 'ספנות' (seamanship) topic — a ship's wheel, so
// questions without a dedicated scene (see getScene's 'ספנות' branch) at
// least get something seamanship-themed instead of silently reusing 'ניווט'.
'ספנות': `
  <rect width="360" height="420" fill="#080f1a"/>
  <circle cx="50" cy="40" r="1.5" fill="white" opacity="0.7"/><circle cx="300" cy="60" r="1" fill="white" opacity="0.6"/><circle cx="320" cy="25" r="1.2" fill="white" opacity="0.8"/>
  <circle cx="180" cy="180" r="92" fill="none" stroke="#2a5a7a" stroke-width="6"/>
  <circle cx="180" cy="180" r="92" fill="none" stroke="#1a3050" stroke-width="2"/>
  ${[0,45,90,135,180,225,270,315].map(d=>{
    const rd=d*Math.PI/180, x1=180+92*Math.sin(rd), y1=180-92*Math.cos(rd), x2=180+118*Math.sin(rd), y2=180-118*Math.cos(rd);
    return `<line x1="${x1.toFixed(1)}" y1="${y1.toFixed(1)}" x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}" stroke="#4a90d9" stroke-width="6" stroke-linecap="round"/><circle cx="${x2.toFixed(1)}" cy="${y2.toFixed(1)}" r="6" fill="#2a5a7a"/>`;
  }).join('')}
  <circle cx="180" cy="180" r="22" fill="#0d2040" stroke="#4a90d9" stroke-width="3"/>
  <circle cx="180" cy="180" r="6" fill="#7eb8f7"/>
  <rect x="48" y="318" width="264" height="44" rx="8" fill="#0d1e38" stroke="#4a90d9" stroke-width="1.5"/>
  <text x="180" y="346" text-anchor="middle" fill="#7eb8f7" font-size="14" font-family="Heebo,sans-serif" font-weight="900">ספנות</text>
  <text x="180" y="398" text-anchor="middle" fill="#4a8ac0" font-size="10" font-family="Heebo,sans-serif">ידע ספנות כללי</text>
`,

'מכ"מ': `
  <rect width="360" height="420" fill="#030a08"/>
  <circle cx="180" cy="180" r="140" fill="#050f0a" stroke="#0a2a18" stroke-width="1"/>
  <circle cx="180" cy="180" r="105" fill="none" stroke="#0a2a18" stroke-width="1"/>
  <circle cx="180" cy="180" r="70" fill="none" stroke="#0a2a18" stroke-width="1"/>
  <circle cx="180" cy="180" r="35" fill="none" stroke="#0a2a18" stroke-width="1"/>
  <line x1="180" y1="40" x2="180" y2="320" stroke="#0a2a18" stroke-width="1"/>
  <line x1="40" y1="180" x2="320" y2="180" stroke="#0a2a18" stroke-width="1"/>
  <g>
    <animateTransform attributeName="transform" type="rotate" values="0 180 180;360 180 180" dur="3s" repeatCount="indefinite"/>
    <line x1="180" y1="180" x2="180" y2="42" stroke="#2ecc71" stroke-width="2" opacity="0.9"/>
    <path d="M180,180 L180,42 A138,138 0 0,1 228,65 Z" fill="#2ecc71" opacity="0.12"/>
  </g>
  <circle cx="130" cy="120" r="5" fill="#2ecc71" opacity="0.8"><animate attributeName="opacity" values="0.8;0.1;0.8" dur="3s" repeatCount="indefinite"/></circle>
  <circle cx="240" cy="150" r="4" fill="#2ecc71" opacity="0.6"><animate attributeName="opacity" values="0.6;0.1;0.6" dur="3s" repeatCount="indefinite" begin="0.5s"/></circle>
  <circle cx="200" cy="230" r="3" fill="#2ecc71" opacity="0.7"><animate attributeName="opacity" values="0.7;0.1;0.7" dur="3s" repeatCount="indefinite" begin="1.2s"/></circle>
  <circle cx="180" cy="180" r="4" fill="#2ecc71"/>
  <text x="180" y="380" text-anchor="middle" fill="#2ecc71" font-size="10" font-family="Heebo,sans-serif" opacity="0.8">Radar — מכ"מ</text>
`,

'ציוד הצלה': `
  <rect width="360" height="420" fill="#0a1020"/>
  <circle cx="180" cy="165" r="80" fill="none" stroke="#e74c3c" stroke-width="8"/>
  <circle cx="180" cy="165" r="80" fill="none" stroke="#fff" stroke-width="4" stroke-dasharray="80,80" stroke-dashoffset="40"/>
  <circle cx="180" cy="165" r="50" fill="#0a1020"/>
  <line x1="180" y1="85" x2="180" y2="55" stroke="#aaa" stroke-width="3"/>
  <line x1="260" y1="165" x2="290" y2="165" stroke="#aaa" stroke-width="3"/>
  <line x1="180" y1="245" x2="180" y2="275" stroke="#aaa" stroke-width="3"/>
  <line x1="100" y1="165" x2="70" y2="165" stroke="#aaa" stroke-width="3"/>
  <text x="180" y="172" text-anchor="middle" fill="#fff" font-size="14" font-family="Arial" font-weight="900">LIFE</text>
  <text x="180" y="185" text-anchor="middle" fill="#fff" font-size="10" font-family="Arial">RING</text>
  <circle cx="180" cy="165" r="80" fill="none" stroke="#e74c3c" stroke-width="3" opacity="0"><animate attributeName="r" values="82;100;82" dur="2s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.6;0;0.6" dur="2s" repeatCount="indefinite"/></circle>
  <rect x="40" y="300" width="280" height="25" rx="5" fill="#1a0000" stroke="#e74c3c" stroke-width="1"/>
  <text x="180" y="317" text-anchor="middle" fill="#e74c3c" font-size="11" font-family="Heebo,sans-serif" font-weight="700">EPIRB · SART · Life Jacket · Flares</text>
  <text x="180" y="380" text-anchor="middle" fill="#c0392b" font-size="10" font-family="Heebo,sans-serif">ציוד הצלה ימי</text>
`,

'אותות מצוקה': `
  <rect width="360" height="420" fill="#0a0a14"/>
  <text x="180" y="100" text-anchor="middle" fill="#e74c3c" font-size="48" font-family="Arial" font-weight="900" opacity="0.9">
    <animate attributeName="opacity" values="0.9;0.2;0.9" dur="1.2s" repeatCount="indefinite"/>
    MAYDAY
  </text>
  <text x="180" y="130" text-anchor="middle" fill="#e74c3c" font-size="14" font-family="Arial" font-weight="700">MAYDAY  MAYDAY</text>
  <line x1="40" y1="150" x2="320" y2="150" stroke="#e74c3c" stroke-width="1" opacity="0.4"/>
  <rect x="80" y="165" width="200" height="85" rx="8" fill="#140a0a" stroke="#e74c3c" stroke-width="1.5"/>
  <text x="180" y="185" text-anchor="middle" fill="#7eb8f7" font-size="10" font-family="Heebo,sans-serif">ערוץ: </text>
  <text x="230" y="185" fill="#fff" font-size="10" font-family="Arial">CH 16 — 156.8MHz</text>
  <text x="180" y="203" text-anchor="middle" fill="#7eb8f7" font-size="10" font-family="Heebo,sans-serif">DSC: </text>
  <text x="215" y="203" fill="#fff" font-size="10" font-family="Arial">Channel 70</text>
  <text x="180" y="221" text-anchor="middle" fill="#7eb8f7" font-size="10" font-family="Heebo,sans-serif">EPIRB: </text>
  <text x="220" y="221" fill="#fff" font-size="10" font-family="Arial">406 MHz</text>
  <text x="180" y="239" text-anchor="middle" fill="#7eb8f7" font-size="10" font-family="Heebo,sans-serif">SART: </text>
  <text x="214" y="239" fill="#fff" font-size="10" font-family="Arial">9 GHz X-band</text>
  <circle cx="180" cy="310" r="35" fill="#3d0000" stroke="#e74c3c" stroke-width="2">
    <animate attributeName="fill" values="#3d0000;#7a0000;#3d0000" dur="1.2s" repeatCount="indefinite"/>
  </circle>
  <text x="180" y="305" text-anchor="middle" fill="#fff" font-size="20">🆘</text>
  <text x="180" y="322" text-anchor="middle" fill="#e74c3c" font-size="10" font-family="Arial" font-weight="700">SOS</text>
  <text x="180" y="390" text-anchor="middle" fill="#c0392b" font-size="10" font-family="Heebo,sans-serif">אותות מצוקה בינלאומיים</text>
`,

'אותות קוליים': `
  <rect width="360" height="420" fill="#050d1a"/>
  <!-- stars -->
  <circle cx="40" cy="25" r="1" fill="white" opacity=".5"/>
  <circle cx="110" cy="15" r="1.2" fill="white" opacity=".6"/>
  <circle cx="200" cy="30" r="1" fill="white" opacity=".4"/>
  <circle cx="290" cy="18" r="1.3" fill="white" opacity=".7"/>
  <circle cx="330" cy="40" r="1" fill="white" opacity=".5"/>
  <!-- sea -->
  <rect x="0" y="310" width="360" height="110" fill="#0a1f3a"/>
  <path d="M0 315 Q60 308 120 315 Q180 322 240 315 Q300 308 360 315" fill="none" stroke="#1a4a6a" stroke-width="1.5" opacity=".6"/>
  <path d="M0 330 Q90 322 180 330 Q270 338 360 330" fill="none" stroke="#1a4a6a" stroke-width="1" opacity=".4"/>
  <!-- ship hull -->
  <ellipse cx="180" cy="312" rx="80" ry="14" fill="#1a2f5e" stroke="#2a4a8a" stroke-width="1.5"/>
  <rect x="120" y="270" width="120" height="44" rx="4" fill="#1a2f5e" stroke="#2a4a8a" stroke-width="1.5"/>
  <!-- bridge -->
  <rect x="148" y="248" width="64" height="26" rx="3" fill="#1e3a6e" stroke="#2a5080" stroke-width="1"/>
  <!-- mast -->
  <line x1="180" y1="150" x2="180" y2="248" stroke="#3a5a8a" stroke-width="2"/>
  <!-- horn / whistle on mast -->
  <rect x="163" y="170" width="22" height="12" rx="3" fill="#4a90d9"/>
  <polygon points="185,170 198,165 198,182 185,182" fill="#357abd"/>
  <text x="202" y="181" fill="#7eb8f7" font-size="9" font-family="Arial" font-weight="700">📯</text>
  <!-- animated sound waves -->
  <g transform="translate(196,176)">
    <path d="M0,0 Q12,-12 12,0 Q12,12 0,0" fill="none" stroke="#4a90d9" stroke-width="2" opacity="0">
      <animate attributeName="opacity" values="0;0.9;0" dur="1.8s" repeatCount="indefinite" begin="0s"/>
      <animate attributeName="d" values="M0,0 Q8,-8 8,0 Q8,8 0,0;M0,0 Q16,-16 16,0 Q16,16 0,0;M0,0 Q8,-8 8,0 Q8,8 0,0" dur="1.8s" repeatCount="indefinite" begin="0s"/>
    </path>
    <path d="M0,0 Q22,-22 22,0 Q22,22 0,0" fill="none" stroke="#7eb8f7" stroke-width="1.5" opacity="0">
      <animate attributeName="opacity" values="0;0.7;0" dur="1.8s" repeatCount="indefinite" begin="0.3s"/>
      <animate attributeName="d" values="M0,0 Q14,-14 14,0 Q14,14 0,0;M0,0 Q28,-28 28,0 Q28,28 0,0;M0,0 Q14,-14 14,0 Q14,14 0,0" dur="1.8s" repeatCount="indefinite" begin="0.3s"/>
    </path>
    <path d="M0,0 Q36,-36 36,0 Q36,36 0,0" fill="none" stroke="#b0d4f0" stroke-width="1" opacity="0">
      <animate attributeName="opacity" values="0;0.5;0" dur="1.8s" repeatCount="indefinite" begin="0.6s"/>
      <animate attributeName="d" values="M0,0 Q20,-20 20,0 Q20,20 0,0;M0,0 Q40,-40 40,0 Q40,40 0,0;M0,0 Q20,-20 20,0 Q20,20 0,0" dur="1.8s" repeatCount="indefinite" begin="0.6s"/>
    </path>
  </g>
  <!-- signal pattern key -->
  <rect x="20" y="78" width="320" height="80" rx="8" fill="#0c1a3a" stroke="#1e3a6e" stroke-width="1" opacity=".9"/>
  <text x="180" y="97" text-anchor="middle" fill="#7eb8f7" font-size="10" font-family="Heebo,sans-serif" font-weight="700">אותות קוליים — COLREGS</text>
  <text x="30" y="116" fill="#4a90d9" font-size="9" font-family="Arial">━</text><text x="42" y="116" fill="#aac4e8" font-size="9" font-family="Heebo,sans-serif"> = פניה ימינה</text>
  <text x="165" y="116" fill="#4a90d9" font-size="9" font-family="Arial">━ ━</text><text x="185" y="116" fill="#aac4e8" font-size="9" font-family="Heebo,sans-serif"> = פניה שמאלה</text>
  <text x="30" y="133" fill="#4a90d9" font-size="9" font-family="Arial">━ ━ ━</text><text x="60" y="133" fill="#aac4e8" font-size="9" font-family="Heebo,sans-serif"> = מנוע אחורה</text>
  <text x="165" y="133" fill="#e74c3c" font-size="9" font-family="Arial">• • • • •</text><text x="195" y="133" fill="#e74c3c" font-size="9" font-family="Heebo,sans-serif"> = סכנה!</text>
  <text x="30" y="150" fill="#2ecc71" font-size="9" font-family="Arial">• = קצרה  ━ = ארוכה</text>
  <text x="180" y="395" text-anchor="middle" fill="#4a90d9" font-size="10" font-family="Heebo,sans-serif">🔊 אותות קוליים — COLREGS</text>
`
});

// ── Question-aware specialized scenes ───────────────────────────────────────

// ── Question-aware specialized scenes ───────────────────────────────────────
const SCENES_QA = {};

// מרקטור — מדידת מרחקים על קנה המידה הצדי
SCENES_QA['mercator_distance'] = `
  <rect width="360" height="420" fill="#0a1a30"/>

  <!-- Chart frame -->
  <rect x="55" y="18" width="250" height="230" rx="4" fill="#0d2040" stroke="#2a4a6a" stroke-width="1.5"/>

  <!-- Latitude gridlines (horizontal) -->
  ${[0,1,2,3,4,5,6,7].map(i=>`
    <line x1="55" y1="${18+i*32}" x2="305" y2="${18+i*32}" stroke="#1a3a58" stroke-width="${i%2===0?1:0.5}"/>
    <text x="51" y="${23+i*32}" text-anchor="end" fill="#7eb8f7" font-size="7.5" font-family="Arial">${36-i}°N</text>
    <text x="309" y="${23+i*32}" fill="#7eb8f7" font-size="7.5" font-family="Arial">${36-i}°N</text>
  `).join('')}

  <!-- Longitude gridlines (vertical) -->
  ${[0,1,2,3,4].map(i=>`
    <line x1="${55+i*62}" y1="18" x2="${55+i*62}" y2="248" stroke="#1a3a58" stroke-width="0.6"/>
    <text x="${55+i*62}" y="258" text-anchor="middle" fill="#4a6a8a" font-size="7" font-family="Arial">${32+i*2}°E</text>
  `).join('')}

  <!-- ✅ LEFT LATITUDE SCALE — highlighted green (correct answer) -->
  <rect x="18" y="18" width="34" height="230" rx="3" fill="#0a3020" stroke="#2ecc71" stroke-width="2">
    <animate attributeName="stroke-opacity" values="1;0.4;1" dur="1.5s" repeatCount="indefinite"/>
  </rect>
  <text x="35" y="12" text-anchor="middle" fill="#2ecc71" font-size="8" font-family="Heebo,sans-serif" font-weight="700">✓ מד פה</text>
  ${[0,1,2,3,4,5,6,7].map(i=>`
    <line x1="18" y1="${18+i*32}" x2="28" y2="${18+i*32}" stroke="#2ecc71" stroke-width="1.5"/>
    <text x="17" y="${23+i*32}" text-anchor="end" fill="#2ecc71" font-size="7" font-family="Arial">${36-i}°</text>
  `).join('')}

  <!-- ❌ BOTTOM LONGITUDE SCALE — red X (wrong) -->
  <rect x="55" y="252" width="250" height="20" rx="3" fill="#2a0808" stroke="#e74c3c" stroke-width="1.5"/>
  <text x="180" y="265" text-anchor="middle" fill="#e74c3c" font-size="9" font-family="Heebo,sans-serif" font-weight="700">✗ לא מודדים כאן — קווי אורך</text>

  <!-- Dividers tool on the side scale (animated) -->
  <g>
    <animate attributeName="opacity" values="0;1;1;0;0" dur="4s" repeatCount="indefinite" keyTimes="0;0.15;0.7;0.85;1"/>
    <!-- divider body -->
    <line x1="35" y1="82" x2="35" y2="146" stroke="#f39c12" stroke-width="2.5" stroke-linecap="round"/>
    <line x1="28" y1="82" x2="42" y2="82" stroke="#f39c12" stroke-width="2" stroke-linecap="round"/>
    <line x1="28" y1="146" x2="42" y2="146" stroke="#f39c12" stroke-width="2" stroke-linecap="round"/>
    <!-- measurement label -->
    <rect x="44" y="103" width="62" height="18" rx="4" fill="#1a3020" stroke="#f39c12" stroke-width="1"/>
    <text x="75" y="115" text-anchor="middle" fill="#f39c12" font-size="8.5" font-family="Arial" font-weight="700">= 2° = 120 NM</text>
  </g>

  <!-- Arrow pointing to side scale -->
  <path d="M82,290 L35,180" stroke="#2ecc71" stroke-width="2" stroke-dasharray="5,3" marker-end="url(#arr)">
    <animate attributeName="opacity" values="0.4;1;0.4" dur="2s" repeatCount="indefinite"/>
  </path>
  <defs><marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#2ecc71"/></marker></defs>

  <!-- Explanation box -->
  <rect x="18" y="278" width="324" height="56" rx="7" fill="#0a1e0f" stroke="#2ecc71" stroke-width="1.5"/>
  <text x="180" y="296" text-anchor="middle" fill="#2ecc71" font-size="11" font-family="Heebo,sans-serif" font-weight="900">מודדים על קנה המידה הצדי</text>
  <text x="180" y="312" text-anchor="middle" fill="#aaa" font-size="10" font-family="Heebo,sans-serif">קווי רוחב = 1° = 60 מייל ימי (NM)</text>
  <text x="180" y="326" text-anchor="middle" fill="#aaa" font-size="9.5" font-family="Heebo,sans-serif">באותו רוחב גיאוגרפי כמו המדידה</text>

  <text x="180" y="390" text-anchor="middle" fill="#4a8ac0" font-size="10" font-family="Heebo,sans-serif">מפת מרקטור — מדידת מרחקים</text>
`;

// ── All navigation question-specific scenes ──────────────────────────────────
Object.assign(SCENES_QA, {

// Q101: Lat/Lon grid defines unique intersection points
'geo_grid': `
  <rect width="360" height="420" fill="#0a1a30"/>
  ${[0,1,2,3,4].map(i=>`<line x1="42" y1="${55+i*45}" x2="318" y2="${55+i*45}" stroke="#1e3a58" stroke-width="${i===2?1.5:.7}"/><text x="39" y="${59+i*45}" text-anchor="end" fill="#4a7aa0" font-size="8" font-family="Arial">${34-i*2}°N</text>`).join('')}
  ${[0,1,2,3,4,5].map(i=>`<line x1="${42+i*55}" y1="55" x2="${42+i*55}" y2="235" stroke="#1e3a58" stroke-width="${i===2?1.5:.7}"/><text x="${42+i*55}" y="247" text-anchor="middle" fill="#4a7aa0" font-size="8" font-family="Arial">${30+i*2}°E</text>`).join('')}
  <circle cx="152" cy="145" r="10" fill="#2ecc71" opacity="0.25"/>
  <circle cx="152" cy="145" r="5" fill="#2ecc71"/>
  <line x1="42" y1="145" x2="152" y2="145" stroke="#2ecc71" stroke-width="1.5" stroke-dasharray="4,3"/>
  <line x1="152" y1="55" x2="152" y2="145" stroke="#2ecc71" stroke-width="1.5" stroke-dasharray="4,3"/>
  <rect x="158" y="125" width="120" height="32" rx="5" fill="#0a2820" stroke="#2ecc71" stroke-width="1"/>
  <text x="218" y="141" text-anchor="middle" fill="#2ecc71" font-size="10.5" font-family="Arial" font-weight="700">32°N, 34°E</text>
  <text x="218" y="153" text-anchor="middle" fill="#aaa" font-size="8.5" font-family="Heebo,sans-serif">תל אביב</text>
  <rect x="18" y="267" width="324" height="60" rx="7" fill="#0d1e38" stroke="#2ecc71" stroke-width="1.5"/>
  <text x="180" y="288" text-anchor="middle" fill="#2ecc71" font-size="12" font-family="Heebo,sans-serif" font-weight="900">קו אורך + קו רוחב = נקודה ייחודית</text>
  <text x="180" y="306" text-anchor="middle" fill="#aaa" font-size="10" font-family="Heebo,sans-serif">כל אתר בעולם מוגדר ע"י חיתוך שני הקווים</text>
  <text x="180" y="322" text-anchor="middle" fill="#7eb8f7" font-size="9.5" font-family="Heebo,sans-serif">(קווי האורך והרוחב לא למדידת מרחקים)</text>
  <text x="180" y="398" text-anchor="middle" fill="#4a8ac0" font-size="10" font-family="Heebo,sans-serif">הרשת הגיאוגרפית</text>
`,

// Q102, Q168: Earth rotates W→E → sun rises east
// Sun fixed in the center (large); Earth (small) orbits it on an ellipse while
// also spinning on its own axis — matches the fix-request from Q102 (no static
// orbiting arrow; the globe itself must visibly rotate).
'earth_rotation': `
  <rect width="360" height="420" fill="#050a18"/>
  <circle cx="48" cy="20" r="1" fill="white" opacity=".5"/>
  <circle cx="320" cy="35" r="1.2" fill="white" opacity=".6"/>
  <circle cx="30" cy="380" r="1" fill="white" opacity=".4"/>
  <circle cx="335" cy="350" r="1.3" fill="white" opacity=".5"/>

  <ellipse cx="180" cy="205" rx="150" ry="78" fill="none" stroke="#3a5a8a" stroke-width="1.5" opacity=".55"/>

  <defs>
    <radialGradient id="sunGrad" cx="38%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#fff6c8"/>
      <stop offset="60%" stop-color="#f1c40f"/>
      <stop offset="100%" stop-color="#e08e0b"/>
    </radialGradient>
    <radialGradient id="earthGrad" cx="35%" cy="32%" r="70%">
      <stop offset="0%" stop-color="#a9c9e8"/>
      <stop offset="100%" stop-color="#3a6ea5"/>
    </radialGradient>
    <clipPath id="earthClip2"><circle cx="0" cy="0" r="22"/></clipPath>
  </defs>
  <circle cx="180" cy="205" r="50" fill="#f1c40f" opacity=".16"/>
  <circle cx="180" cy="205" r="38" fill="url(#sunGrad)"/>

  <g>
    <animateMotion dur="10s" repeatCount="indefinite" rotate="0">
      <mpath href="#orbitPath"/>
    </animateMotion>
    <circle r="22" fill="url(#earthGrad)" stroke="#1e4a7a" stroke-width="1"/>
    <g clip-path="url(#earthClip2)">
      <g>
        <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="2.4s" repeatCount="indefinite"/>
        <line x1="0" y1="-22" x2="0" y2="22" stroke="#1e4a7a" stroke-width="1.2" opacity=".7"/>
        <ellipse cx="0" cy="0" rx="9" ry="22" fill="none" stroke="#1e4a7a" stroke-width="1" opacity=".6"/>
        <ellipse cx="0" cy="0" rx="18" ry="22" fill="none" stroke="#1e4a7a" stroke-width="1" opacity=".6"/>
      </g>
      <line x1="-22" y1="0" x2="22" y2="0" stroke="#1e4a7a" stroke-width="1" opacity=".5"/>
    </g>
  </g>
  <path id="orbitPath" d="M30,205 A150,78 0 1,1 330,205 A150,78 0 1,1 30,205" fill="none" stroke="none"/>

  <text x="180" y="398" text-anchor="middle" fill="#4a8ac0" font-size="10" font-family="Heebo,sans-serif">כדור הארץ מסתובב סביב צירו וסביב השמש</text>
`,

// Q103, Q171: Polaris altitude = latitude
'polaris': `
  <rect width="360" height="420" fill="#050a18"/>
  <circle cx="180" cy="52" r="9" fill="white"/>
  ${[0,72,144,216,288].map(d=>{const rd=d*Math.PI/180;return `<line x1="${180+9*Math.sin(rd)}" y1="${52-9*Math.cos(rd)}" x2="${180+16*Math.sin(rd)}" y2="${52-16*Math.cos(rd)}" stroke="white" stroke-width="1.5"/>`}).join('')}
  <text x="200" y="50" fill="white" font-size="9" font-family="Heebo,sans-serif">★ כוכב הצפון (Polaris)</text>
  <line x1="20" y1="230" x2="340" y2="230" stroke="#4a8ac0" stroke-width="2"/>
  <text x="345" y="234" fill="#4a8ac0" font-size="9" font-family="Heebo,sans-serif">אופק</text>
  <circle cx="70" cy="230" r="7" fill="#7eb8f7"/>
  <text x="70" y="248" text-anchor="middle" fill="#7eb8f7" font-size="9" font-family="Heebo,sans-serif">צופה</text>
  <line x1="70" y1="230" x2="180" y2="52" stroke="#2ecc71" stroke-width="2" stroke-dasharray="5,3"/>
  <path d="M70,185 A45,45 0 0,1 102,220" fill="none" stroke="#2ecc71" stroke-width="2.5"/>
  <text x="118" y="204" fill="#2ecc71" font-size="17" font-family="Arial" font-weight="900">45°</text>
  <rect x="165" y="140" width="178" height="62" rx="7" fill="#0a2820" stroke="#2ecc71" stroke-width="2"/>
  <text x="254" y="160" text-anchor="middle" fill="#2ecc71" font-size="11" font-family="Heebo,sans-serif" font-weight="900">גובה כוכב הצפון = 45°</text>
  <text x="254" y="177" text-anchor="middle" fill="#fff" font-size="12" font-family="Arial" font-weight="700">→ קו רוחב = 45°N</text>
  <text x="254" y="194" text-anchor="middle" fill="#aaa" font-size="9" font-family="Heebo,sans-serif">זווית קבועה = הפלגה על קו רוחב קבוע</text>
  <rect x="18" y="278" width="324" height="50" rx="7" fill="#0d1e38" stroke="#7eb8f7" stroke-width="1.5"/>
  <text x="180" y="298" text-anchor="middle" fill="#7eb8f7" font-size="11" font-family="Heebo,sans-serif" font-weight="900">גובה כוכב הצפון מעל האופק = קו הרוחב</text>
  <text x="180" y="316" text-anchor="middle" fill="#aaa" font-size="10" font-family="Heebo,sans-serif">מודדים כל ערב: זווית קבועה = קו רוחב קבוע</text>
  <text x="180" y="398" text-anchor="middle" fill="#4a8ac0" font-size="10" font-family="Heebo,sans-serif">ניווט בכוכב הצפון</text>
`,

// Q107, Q115: Nautical mile = 1' arc on great circle (meridian) = 1852m.
// Polar (top-down, from the North Pole) view: meridians are real straight
// radii from the pole, so the 20° angle between 0° and 20°00' is drawn true,
// and the 20°00'→20°01' gap (1' of arc = 1 NM) is exaggerated for visibility.
'nautical_mile': `
  <rect width="360" height="420" fill="#ffffff"/>
  <text x="180" y="26" text-anchor="middle" fill="#000" font-size="13" font-family="Heebo,sans-serif" font-weight="700">מייל ימי = לאורך הקשת שבין קו אורך</text>
  <text x="180" y="46" text-anchor="middle" fill="#000" font-size="13" font-family="Heebo,sans-serif" font-weight="700">°20 01' לבין קו אורך °20 00'</text>
  <defs>
    <radialGradient id="earthGrad" cx="38%" cy="32%" r="75%">
      <stop offset="0%" stop-color="#bfe3ff"/>
      <stop offset="55%" stop-color="#6fb6e8"/>
      <stop offset="100%" stop-color="#2a6aa8"/>
    </radialGradient>
  </defs>
  <circle cx="180" cy="245" r="135" fill="url(#earthGrad)" stroke="#000" stroke-width="1.6"/>
  <circle cx="180" cy="245" r="95" fill="none" stroke="#1a3a5a" stroke-width="0.8" opacity="0.45"/>
  <circle cx="180" cy="245" r="50" fill="none" stroke="#1a3a5a" stroke-width="0.8" opacity="0.4"/>
  <path d="M95,185 Q75,225 100,265 Q70,285 105,320 Q90,345 130,355 Q170,335 150,300 Q175,280 155,250 Q175,220 145,195 Q120,175 95,185Z" fill="#3a7a3a" opacity="0.85"/>
  <path d="M250,150 Q280,175 265,210 Q295,230 270,260 Q290,285 255,295 Q235,270 250,240 Q225,215 245,190 Q230,165 250,150Z" fill="#3a7a3a" opacity="0.7"/>
  <circle cx="180" cy="245" r="3.5" fill="#000"/>
  <text x="180" y="262" text-anchor="middle" fill="#000" font-size="8" font-family="Heebo,sans-serif" font-weight="700">קוטב צפוני</text>
  <line x1="180" y1="245" x2="180" y2="113" stroke="#777" stroke-width="1.2" stroke-dasharray="4,3"/>
  <text x="170" y="105" text-anchor="end" fill="#777" font-size="10" font-family="Arial">קו אורך 00°00'</text>
  <line x1="180" y1="245" x2="226" y2="118" stroke="#000" stroke-width="2"/>
  <text x="232" y="112" fill="#000" font-size="12" font-family="Arial" font-weight="700">קו אורך 20°00'</text>
  <path d="M180,165 A88,88 0 0,1 213,178" fill="none" stroke="#000" stroke-width="1.2"/>
  <text x="195" y="155" fill="#000" font-size="11" font-family="Arial" font-weight="700">20°</text>
  <line x1="180" y1="245" x2="243" y2="126" stroke="#c0392b" stroke-width="2.5"/>
  <text x="248" y="128" fill="#c0392b" font-size="12" font-family="Arial" font-weight="700">'קו אורך 01 °20</text>
  <path d="M226,118 A135,135 0 0,1 243,126" fill="none" stroke="#c0392b" stroke-width="3.5"/>
  <line x1="318" y1="160" x2="236" y2="122" stroke="#c0392b" stroke-width="1.3"/>
  <text x="320" y="164" fill="#c0392b" font-size="13" font-family="Heebo,sans-serif" font-weight="700">מייל 1</text>
`,

// Q112: Speed calculation 15m/5s = 5.83 kn
'speed_calc': `
  <rect width="360" height="420" fill="#080f1a"/>
  <path d="M20,160 L295,160 L330,178 L295,196 L20,196 Z" fill="#0d2a4e" stroke="#2a6aae" stroke-width="2"/>
  <circle cx="328" cy="178" r="5" fill="#e74c3c"/>
  <text x="345" y="182" fill="#e74c3c" font-size="9" font-family="Heebo,sans-serif">חרטום</text>
  <circle cx="22" cy="178" r="5" fill="#7eb8f7"/>
  <text x="8" y="170" fill="#7eb8f7" font-size="9" font-family="Heebo,sans-serif">ירכ'</text>
  <line x1="22" y1="200" x2="328" y2="200" stroke="#f39c12" stroke-width="1.5"/>
  <text x="175" y="215" text-anchor="middle" fill="#f39c12" font-size="12" font-family="Arial" font-weight="700">← 15 מטר →</text>
  <circle cx="305" cy="148" r="5" fill="#2ecc71"/>
  <path d="M305,148 L42,148" stroke="#2ecc71" stroke-width="1.5" stroke-dasharray="6,3" marker-end="url(#bkArr)"/>
  <defs><marker id="bkArr" markerWidth="8" markerHeight="8" refX="0" refY="3" orient="auto"><path d="M8,0 L0,3 L8,6" fill="none" stroke="#2ecc71" stroke-width="2"/></marker></defs>
  <text x="175" y="143" text-anchor="middle" fill="#2ecc71" font-size="10" font-family="Heebo,sans-serif">⏱ 5 שניות</text>
  <rect x="18" y="228" width="324" height="115" rx="8" fill="#0d1e38" stroke="#f39c12" stroke-width="1.5"/>
  <text x="180" y="250" text-anchor="middle" fill="#f39c12" font-size="12" font-family="Heebo,sans-serif" font-weight="700">חישוב מהירות:</text>
  <text x="180" y="270" text-anchor="middle" fill="#fff" font-size="12" font-family="Arial">v = 15m ÷ 5s = 3 m/s</text>
  <text x="180" y="290" text-anchor="middle" fill="#fff" font-size="12" font-family="Arial">3 m/s × 3600 ÷ 1852</text>
  <line x1="50" y1="300" x2="310" y2="300" stroke="#f39c12" stroke-width="0.8" opacity="0.5"/>
  <text x="180" y="322" text-anchor="middle" fill="#2ecc71" font-size="20" font-family="Arial" font-weight="900">= 5.83 קשרים</text>
  <text x="180" y="338" text-anchor="middle" fill="#aaa" font-size="10" font-family="Heebo,sans-serif">תשובה ד׳ — הנוסחה: v(kn) = m/s × 3.6 ÷ 1.852</text>
  <text x="180" y="398" text-anchor="middle" fill="#4a8ac0" font-size="10" font-family="Heebo,sans-serif">מדידת מהירות בשיטת הבולין</text>
`,

// Q117: Horizon distance d = 2.03 × √h
'horizon_dist': `
  <rect width="360" height="420" fill="#060d18"/>
  <path d="M0,260 Q180,228 360,260" fill="#0a1a2a" stroke="#2a6aae" stroke-width="2"/>
  <rect x="0" y="260" width="360" height="80" fill="#0a1a2a"/>
  <line x1="50" y1="260" x2="50" y2="210" stroke="#f39c12" stroke-width="2.5"/>
  <circle cx="50" cy="206" r="7" fill="#f39c12"/>
  <text x="65" y="214" fill="#f39c12" font-size="11" font-family="Arial" font-weight="700">h = 9m</text>
  <line x1="42" y1="260" x2="58" y2="260" stroke="#f39c12" stroke-width="1.5"/>
  <line x1="42" y1="210" x2="58" y2="210" stroke="#f39c12" stroke-width="1.5"/>
  <line x1="50" y1="206" x2="295" y2="242" stroke="#2ecc71" stroke-width="2.5" stroke-dasharray="5,3"/>
  <circle cx="295" cy="243" r="6" fill="#2ecc71"/>
  <text x="300" y="238" fill="#2ecc71" font-size="9" font-family="Heebo,sans-serif">אופק</text>
  <line x1="50" y1="263" x2="295" y2="263" stroke="#2ecc71" stroke-width="1.5"/>
  <text x="172" y="277" text-anchor="middle" fill="#2ecc71" font-size="12" font-family="Arial" font-weight="700">≈ 6.1 NM</text>
  <rect x="18" y="298" width="324" height="68" rx="8" fill="#0d1e38" stroke="#2ecc71" stroke-width="1.5"/>
  <text x="180" y="318" text-anchor="middle" fill="#2ecc71" font-size="12" font-family="Heebo,sans-serif" font-weight="900">נוסחת מרחק האופק:</text>
  <text x="180" y="338" text-anchor="middle" fill="#fff" font-size="13" font-family="Arial" font-weight="700">d(NM) = 2.03 × √h(m)</text>
  <text x="180" y="358" text-anchor="middle" fill="#f39c12" font-size="13" font-family="Arial" font-weight="700">= 2.03 × √9 = 2.03 × 3 ≈ 6.1</text>
  <text x="180" y="398" text-anchor="middle" fill="#4a8ac0" font-size="10" font-family="Heebo,sans-serif">מרחק האופק</text>
`,

// Q109: Local Time = longitude / 15 → hours from UTC
'local_time': `
  <rect width="360" height="420" fill="#080f1a"/>
  <line x1="180" y1="25" x2="180" y2="245" stroke="#f39c12" stroke-width="2" stroke-dasharray="5,3"/>
  <text x="180" y="20" text-anchor="middle" fill="#f39c12" font-size="9" font-family="Arial" font-weight="700">0° גרינוויץ (UTC)</text>
  ${[-2,-1,0,1,2].map(i=>`
    <rect x="${80+i*40}" y="40" width="38" height="190" fill="${i===0?'#0d2a3e':'#0a1525'}" stroke="${i===0?'#f39c12':'#1a3050'}" stroke-width="${i===0?2:0.8}" rx="2"/>
    <text x="${99+i*40}" y="58" text-anchor="middle" fill="${i===0?'#f39c12':'#4a6a8a'}" font-size="8" font-family="Arial">UTC${i===0?'':i>0?'+'+i:i}</text>
    <text x="${99+i*40}" y="72" text-anchor="middle" fill="${i===0?'#f39c12':'#4a6a8a'}" font-size="7" font-family="Arial">${i*15}°</text>
  `).join('')}
  <rect x="80" y="100" width="38" height="60" rx="3" fill="#0a2820" stroke="#2ecc71" stroke-width="1.5"/>
  <text x="99" y="118" text-anchor="middle" fill="#2ecc71" font-size="8" font-family="Heebo,sans-serif">34°E</text>
  <text x="99" y="132" text-anchor="middle" fill="#2ecc71" font-size="8" font-family="Heebo,sans-serif">≈ UTC+2</text>
  <text x="99" y="148" text-anchor="middle" fill="#2ecc71" font-size="7" font-family="Heebo,sans-serif">ישראל</text>
  <text x="99" y="162" text-anchor="middle" fill="#f39c12" font-size="7.5" font-family="Arial">+2h</text>
  <path d="M50,178 L340,178" stroke="#1a3a5a" stroke-width="1"/>
  <text x="340" y="195" fill="#7eb8f7" font-size="9" font-family="Heebo,sans-serif">→ מזרח = קדימה</text>
  <text x="20" y="195" fill="#7eb8f7" font-size="9" font-family="Heebo,sans-serif">מערב = אחורה ←</text>
  <rect x="18" y="258" width="324" height="68" rx="7" fill="#0d1e38" stroke="#f39c12" stroke-width="1.5"/>
  <text x="180" y="278" text-anchor="middle" fill="#f39c12" font-size="12" font-family="Heebo,sans-serif" font-weight="900">זמן מקומי לפי קו האורך</text>
  <text x="180" y="296" text-anchor="middle" fill="#fff" font-size="11" font-family="Arial">כל 15° = שעה אחת</text>
  <text x="180" y="314" text-anchor="middle" fill="#7eb8f7" font-size="10.5" font-family="Heebo,sans-serif">מזרחה: +שעות | מערבה: −שעות מ-UTC</text>
  <text x="180" y="398" text-anchor="middle" fill="#4a8ac0" font-size="10" font-family="Heebo,sans-serif">זמן מקומי (Local Time)</text>
`,

// Q114: Zone Time = ±7.5° from central meridian = 15° wide strip
'zone_time': `
  <rect width="360" height="420" fill="#080f1a"/>
  <rect x="90" y="30" width="180" height="220" rx="4" fill="#0a1828" stroke="#7eb8f7" stroke-width="1.5"/>
  <rect x="90" y="30" width="90" height="220" rx="4" fill="#0d1e38" stroke="#7eb8f7" stroke-width="0.5" opacity="0.4"/>
  <rect x="180" y="30" width="90" height="220" rx="4" fill="#0d1e38" stroke="#7eb8f7" stroke-width="0.5" opacity="0.4"/>
  <line x1="180" y1="25" x2="180" y2="255" stroke="#f39c12" stroke-width="2.5"/>
  <text x="180" y="22" text-anchor="middle" fill="#f39c12" font-size="9" font-family="Arial" font-weight="700">קו אורך מרכזי</text>
  <line x1="90" y1="25" x2="90" y2="255" stroke="#4a8ac0" stroke-width="1.5" stroke-dasharray="4,3"/>
  <line x1="270" y1="25" x2="270" y2="255" stroke="#4a8ac0" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="90" y="265" text-anchor="middle" fill="#4a8ac0" font-size="9" font-family="Arial">−7.5°</text>
  <text x="270" y="265" text-anchor="middle" fill="#4a8ac0" font-size="9" font-family="Arial">+7.5°</text>
  <line x1="90" y1="140" x2="270" y2="140" stroke="#2ecc71" stroke-width="2.5" marker-start="url(#tZL)" marker-end="url(#tZR)"/>
  <defs>
    <marker id="tZL" markerWidth="8" markerHeight="8" refX="8" refY="3" orient="auto"><path d="M8,0 L0,3 L8,6" fill="#2ecc71"/></marker>
    <marker id="tZR" markerWidth="8" markerHeight="8" refX="0" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6" fill="#2ecc71"/></marker>
  </defs>
  <text x="180" y="132" text-anchor="middle" fill="#2ecc71" font-size="13" font-family="Arial" font-weight="700">15°</text>
  <text x="135" y="158" text-anchor="middle" fill="#7eb8f7" font-size="10" font-family="Arial">7.5°</text>
  <text x="225" y="158" text-anchor="middle" fill="#7eb8f7" font-size="10" font-family="Arial">7.5°</text>
  <rect x="18" y="278" width="324" height="68" rx="7" fill="#0d1e38" stroke="#2ecc71" stroke-width="1.5"/>
  <text x="180" y="298" text-anchor="middle" fill="#2ecc71" font-size="12" font-family="Heebo,sans-serif" font-weight="900">אזור זמן = רצועה בת 15°</text>
  <text x="180" y="316" text-anchor="middle" fill="#fff" font-size="11" font-family="Heebo,sans-serif">7.5° מזרחה + 7.5° מערבה לקו המרכזי</text>
  <text x="180" y="334" text-anchor="middle" fill="#7eb8f7" font-size="10" font-family="Heebo,sans-serif">כל האזור שומר על אותו זמן</text>
  <text x="180" y="398" text-anchor="middle" fill="#4a8ac0" font-size="10" font-family="Heebo,sans-serif">Zone Time — אזור זמן</text>
`,

// Q120: International Date Line crossing
'date_line': `
  <rect width="360" height="420" fill="#080f1a"/>
  <line x1="180" y1="20" x2="180" y2="270" stroke="#e74c3c" stroke-width="3" stroke-dasharray="8,4"/>
  <text x="180" y="16" text-anchor="middle" fill="#e74c3c" font-size="9" font-family="Arial" font-weight="700">קו התאריך הבינלאומי 180°</text>
  <rect x="15" y="35" width="155" height="110" rx="7" fill="#0d1e38" stroke="#7eb8f7" stroke-width="1.5"/>
  <text x="92" y="58" text-anchor="middle" fill="#7eb8f7" font-size="10" font-family="Arial" font-weight="700">179°31' E</text>
  <text x="92" y="76" text-anchor="middle" fill="#7eb8f7" font-size="9" font-family="Heebo,sans-serif">UTC +12</text>
  <text x="92" y="102" text-anchor="middle" fill="#fff" font-size="16" font-family="Arial" font-weight="900">23:59</text>
  <text x="92" y="120" text-anchor="middle" fill="#f39c12" font-size="11" font-family="Heebo,sans-serif" font-weight="700">31 דצמבר</text>
  <rect x="190" y="35" width="155" height="110" rx="7" fill="#0d1e38" stroke="#2ecc71" stroke-width="1.5"/>
  <text x="268" y="58" text-anchor="middle" fill="#2ecc71" font-size="10" font-family="Arial" font-weight="700">179°31' W</text>
  <text x="268" y="76" text-anchor="middle" fill="#2ecc71" font-size="9" font-family="Heebo,sans-serif">UTC −12</text>
  <text x="268" y="102" text-anchor="middle" fill="#fff" font-size="16" font-family="Arial" font-weight="900">23:59</text>
  <text x="268" y="120" text-anchor="middle" fill="#2ecc71" font-size="11" font-family="Heebo,sans-serif" font-weight="700">30 דצמבר</text>
  <text x="180" y="200" text-anchor="middle" fill="#e74c3c" font-size="28" font-family="Arial">↔</text>
  <text x="180" y="220" text-anchor="middle" fill="#e74c3c" font-size="10" font-family="Heebo,sans-serif">הפרש 24 שעות = יום שלם</text>
  <rect x="18" y="268" width="324" height="60" rx="7" fill="#0d1e38" stroke="#2ecc71" stroke-width="1.5"/>
  <text x="180" y="288" text-anchor="middle" fill="#2ecc71" font-size="12" font-family="Heebo,sans-serif" font-weight="900">E/W = שעות זהות, תאריך שונה ביום</text>
  <text x="180" y="306" text-anchor="middle" fill="#aaa" font-size="10" font-family="Heebo,sans-serif">מ-E לW: נחזור יום אחורה | מ-W לE: נקפוץ יום קדימה</text>
  <text x="180" y="398" text-anchor="middle" fill="#4a8ac0" font-size="10" font-family="Heebo,sans-serif">קו התאריך הבינלאומי</text>
`,

// Q121: UTC+3 = 3 hours ahead = east of Greenwich
'utc_plus3': `
  <rect width="360" height="420" fill="#080f1a"/>
  <rect x="18" y="30" width="148" height="130" rx="10" fill="#0d1e38" stroke="#7eb8f7" stroke-width="2"/>
  <text x="92" y="60" text-anchor="middle" fill="#7eb8f7" font-size="11" font-family="Heebo,sans-serif" font-weight="700">UTC (גרינוויץ)</text>
  <text x="92" y="80" text-anchor="middle" fill="#7eb8f7" font-size="10" font-family="Arial">0°</text>
  <text x="92" y="132" text-anchor="middle" fill="#fff" font-size="40" font-family="Arial" font-weight="900">06:00</text>
  <rect x="194" y="30" width="148" height="130" rx="10" fill="#0d2820" stroke="#2ecc71" stroke-width="2"/>
  <text x="268" y="60" text-anchor="middle" fill="#2ecc71" font-size="11" font-family="Heebo,sans-serif" font-weight="700">UTC+3</text>
  <text x="268" y="80" text-anchor="middle" fill="#2ecc71" font-size="10" font-family="Arial">45°E</text>
  <text x="268" y="132" text-anchor="middle" fill="#fff" font-size="40" font-family="Arial" font-weight="900">09:00</text>
  <text x="180" y="110" text-anchor="middle" fill="#f39c12" font-size="22" font-family="Arial" font-weight="900">+3h →</text>
  <rect x="18" y="182" width="324" height="90" rx="7" fill="#0d1e38" stroke="#2ecc71" stroke-width="1.5"/>
  <text x="180" y="205" text-anchor="middle" fill="#2ecc71" font-size="12" font-family="Heebo,sans-serif" font-weight="900">UTC+3 — כל 3 הפירושים נכונים:</text>
  <text x="180" y="224" text-anchor="middle" fill="#fff" font-size="10.5" font-family="Heebo,sans-serif">א. אתה נמצא מזרחה לגרינוויץ</text>
  <text x="180" y="242" text-anchor="middle" fill="#fff" font-size="10.5" font-family="Heebo,sans-serif">ב. אם בגרינוויץ 06:00, אצלך 09:00</text>
  <text x="180" y="260" text-anchor="middle" fill="#fff" font-size="10.5" font-family="Heebo,sans-serif">ג. הזמן המקומי מאוחר ב-3h מ-UTC</text>
  <text x="180" y="398" text-anchor="middle" fill="#4a8ac0" font-size="10" font-family="Heebo,sans-serif">UTC+3 — אזור זמן</text>
`,

// Q180: UTC = Coordinated Universal Time = GMT
'utc_def': `
  <rect width="360" height="420" fill="#080f1a"/>
  <circle cx="180" cy="155" r="100" fill="#0d2040" stroke="#2a4a6a" stroke-width="2"/>
  <line x1="180" y1="55" x2="180" y2="255" stroke="#f39c12" stroke-width="2.5" stroke-dasharray="5,3"/>
  <text x="180" y="50" text-anchor="middle" fill="#f39c12" font-size="9" font-family="Heebo,sans-serif">גרינוויץ, לונדון</text>
  <text x="180" y="155" text-anchor="middle" fill="#f39c12" font-size="11" font-family="Arial" font-weight="700">0°</text>
  <text x="85" y="158" text-anchor="middle" fill="#4a6a8a" font-size="9" font-family="Arial">W</text>
  <text x="275" y="158" text-anchor="middle" fill="#4a6a8a" font-size="9" font-family="Arial">E</text>
  <rect x="18" y="278" width="324" height="90" rx="7" fill="#0d1e38" stroke="#f39c12" stroke-width="1.5"/>
  <text x="180" y="300" text-anchor="middle" fill="#f39c12" font-size="13" font-family="Arial" font-weight="900">UTC</text>
  <text x="180" y="320" text-anchor="middle" fill="#fff" font-size="11" font-family="Heebo,sans-serif">Coordinated Universal Time</text>
  <text x="180" y="338" text-anchor="middle" fill="#2ecc71" font-size="12" font-family="Heebo,sans-serif" font-weight="700">= זמן אוניברסלי מתואם = GMT</text>
  <text x="180" y="356" text-anchor="middle" fill="#aaa" font-size="10" font-family="Heebo,sans-serif">בסיס כל חישובי הזמן בניווט ימי</text>
  <text x="180" y="398" text-anchor="middle" fill="#4a8ac0" font-size="10" font-family="Heebo,sans-serif">UTC — זמן אוניברסלי</text>
`,

// Q111: Vessel stationary → apparent wind = true wind
'wind_stationary': `
  <rect width="360" height="420" fill="#080f1a"/>
  <path d="M130,195 L220,195 L230,210 L220,225 L130,225 L120,210 Z" fill="#0d2a4e" stroke="#2a6aae" stroke-width="2"/>
  <text x="175" y="214" text-anchor="middle" fill="#7eb8f7" font-size="9" font-family="Heebo,sans-serif">עוגן ⚓</text>
  <text x="175" y="255" text-anchor="middle" fill="#7eb8f7" font-size="10" font-family="Heebo,sans-serif">ספינה עומדת</text>
  <line x1="180" y1="80" x2="180" y2="175" stroke="#2ecc71" stroke-width="3" stroke-linecap="round" marker-end="url(#wArr)"/>
  <defs><marker id="wArr" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto"><path d="M0,0 L5,10 L10,0 Z" fill="#2ecc71"/></marker></defs>
  <text x="195" y="120" fill="#2ecc71" font-size="11" font-family="Heebo,sans-serif" font-weight="700">רוח אמיתית</text>
  <text x="195" y="136" fill="#2ecc71" font-size="10" font-family="Heebo,sans-serif">(15 קשרים)</text>
  <rect x="18" y="278" width="324" height="75" rx="7" fill="#0d1e38" stroke="#2ecc71" stroke-width="1.5"/>
  <text x="180" y="300" text-anchor="middle" fill="#2ecc71" font-size="12" font-family="Heebo,sans-serif" font-weight="900">ספינה עומדת (v = 0)</text>
  <text x="180" y="320" text-anchor="middle" fill="#fff" font-size="12" font-family="Arial" font-weight="700">רוח יחסית = רוח אמיתית</text>
  <text x="180" y="340" text-anchor="middle" fill="#aaa" font-size="10" font-family="Heebo,sans-serif">מד הרוח מראה את הרוח האמיתית</text>
  <text x="180" y="398" text-anchor="middle" fill="#4a8ac0" font-size="10" font-family="Heebo,sans-serif">רוח אמיתית ויחסית</text>
`,

// Q123: Sailing → wind meter shows apparent (relative) wind
'apparent_wind': `
  <rect width="360" height="420" fill="#080f1a"/>
  <path d="M80,190 L200,190 L220,205 L200,220 L80,220 L62,205 Z" fill="#0d2a4e" stroke="#2a6aae" stroke-width="2"/>
  <path d="M220,170 L320,170" stroke="#f39c12" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#sArr)"/>
  <defs>
    <marker id="sArr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#f39c12"/></marker>
    <marker id="tWA" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#7eb8f7"/></marker>
    <marker id="appA" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#2ecc71"/></marker>
  </defs>
  <text x="330" y="165" fill="#f39c12" font-size="9" font-family="Heebo,sans-serif">→ ספינה 6kn</text>
  <line x1="140" y1="130" x2="140" y2="188" stroke="#7eb8f7" stroke-width="2.5" marker-end="url(#tWA)"/>
  <text x="88" y="145" fill="#7eb8f7" font-size="9" font-family="Heebo,sans-serif">רוח אמיתית↓</text>
  <text x="88" y="158" fill="#7eb8f7" font-size="9" font-family="Heebo,sans-serif">12 קשרים</text>
  <line x1="140" y1="80" x2="68" y2="188" stroke="#2ecc71" stroke-width="3" marker-end="url(#appA)"/>
  <text x="32" y="110" fill="#2ecc71" font-size="9" font-family="Heebo,sans-serif" font-weight="700">רוח יחסית</text>
  <text x="32" y="123" fill="#2ecc71" font-size="9" font-family="Heebo,sans-serif">(מדומה)</text>
  <text x="32" y="136" fill="#2ecc71" font-size="9" font-family="Heebo,sans-serif">≈ 13.4kn</text>
  <circle cx="140" cy="188" r="4" fill="#fff"/>
  <rect x="18" y="258" width="324" height="75" rx="7" fill="#0d1e38" stroke="#2ecc71" stroke-width="1.5"/>
  <text x="180" y="278" text-anchor="middle" fill="#2ecc71" font-size="12" font-family="Heebo,sans-serif" font-weight="900">בהפלגה: מד הרוח מראה רוח יחסית</text>
  <text x="180" y="296" text-anchor="middle" fill="#fff" font-size="11" font-family="Heebo,sans-serif">= וקטור סכום: רוח אמיתית + תנועת ספינה</text>
  <text x="180" y="314" text-anchor="middle" fill="#7eb8f7" font-size="10" font-family="Heebo,sans-serif">תמיד מגיע יותר מקדמה מהרוח האמיתית</text>
  <text x="180" y="398" text-anchor="middle" fill="#4a8ac0" font-size="10" font-family="Heebo,sans-serif">רוח יחסית (Apparent Wind)</text>
`,

// Q113: Magnetic course = angle between keel and magnetic north
'magnetic_course': `
  <rect width="360" height="420" fill="#080f1a"/>
  <circle cx="180" cy="175" r="110" fill="#0c1828" stroke="#1e3a5a" stroke-width="1.5"/>
  ${[0,45,90,135,180,225,270,315].map(d=>{const rd=d*Math.PI/180;const x1=180+104*Math.sin(rd),y1=175-104*Math.cos(rd),x2=180+90*Math.sin(rd),y2=175-90*Math.cos(rd);return `<line x1="${x1.toFixed(1)}" y1="${y1.toFixed(1)}" x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}" stroke="${d===0?'#e74c3c':'#2a5a7a'}" stroke-width="${d===0?2.5:1}"/>`}).join('')}
  <text x="180" y="68" text-anchor="middle" fill="#e74c3c" font-size="13" font-family="Arial" font-weight="900">N מגנטי</text>
  <line x1="180" y1="175" x2="180" y2="75" stroke="#e74c3c" stroke-width="2.5" stroke-dasharray="5,3"/>
  <path d="M220,110 L280,60" stroke="#2ecc71" stroke-width="3" stroke-linecap="round" marker-end="url(#kArr)"/>
  <defs><marker id="kArr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#2ecc71"/></marker></defs>
  <path d="M180,130 A45,45 0 0,1 212,108" fill="none" stroke="#f39c12" stroke-width="2.5"/>
  <text x="218" y="138" fill="#f39c12" font-size="14" font-family="Arial" font-weight="900">045°</text>
  <text x="265" y="55" fill="#2ecc71" font-size="9" font-family="Heebo,sans-serif">שדרת ספינה</text>
  <circle cx="180" cy="175" r="5" fill="#7eb8f7"/>
  <rect x="18" y="305" width="324" height="62" rx="7" fill="#0d1e38" stroke="#f39c12" stroke-width="1.5"/>
  <text x="180" y="326" text-anchor="middle" fill="#f39c12" font-size="12" font-family="Heebo,sans-serif" font-weight="900">קורס מגנטי</text>
  <text x="180" y="345" text-anchor="middle" fill="#fff" font-size="11" font-family="Heebo,sans-serif">= הזווית בין שדרת הספינה לצפון המגנטי</text>
  <text x="180" y="398" text-anchor="middle" fill="#4a8ac0" font-size="10" font-family="Heebo,sans-serif">קורס מגנטי</text>
`,

// Q167: Rhumb Line = constant angle to meridians = straight on Mercator
'rhumb_line': `
  <rect width="360" height="420" fill="#0a1a30"/>
  <rect x="18" y="20" width="324" height="210" rx="5" fill="#0d2040" stroke="#2a4a6a" stroke-width="1.5"/>
  ${[0,1,2,3,4].map(i=>`<line x1="18" y1="${20+i*52}" x2="342" y2="${20+i*52}" stroke="#1a3a58" stroke-width="${i%2===0?.8:.4}"/>`).join('')}
  ${[0,1,2,3,4,5].map(i=>`<line x1="${18+i*64}" y1="20" x2="${18+i*64}" y2="230" stroke="#1a3a58" stroke-width=".6"/>`).join('')}
  <circle cx="60" cy="195" r="5" fill="#f39c12"/>
  <circle cx="300" cy="55" r="5" fill="#f39c12"/>
  <line x1="60" y1="195" x2="300" y2="55" stroke="#2ecc71" stroke-width="3"/>
  <text x="200" y="148" fill="#2ecc71" font-size="11" font-family="Arial" font-weight="700">Rhumb Line</text>
  <text x="200" y="163" fill="#2ecc71" font-size="9" font-family="Heebo,sans-serif">(קו ישר במרקטור)</text>
  <rect x="18" y="248" width="324" height="95" rx="7" fill="#0d1e38" stroke="#2ecc71" stroke-width="1.5"/>
  <text x="180" y="268" text-anchor="middle" fill="#2ecc71" font-size="12" font-family="Heebo,sans-serif" font-weight="900">Rhumb Line (קו ריים)</text>
  <text x="180" y="287" text-anchor="middle" fill="#fff" font-size="10.5" font-family="Heebo,sans-serif">✓ קו ישר על מפת מרקטור</text>
  <text x="180" y="305" text-anchor="middle" fill="#fff" font-size="10.5" font-family="Heebo,sans-serif">✓ חוצה את כל קווי האורך באותה זווית</text>
  <text x="180" y="323" text-anchor="middle" fill="#e74c3c" font-size="10" font-family="Heebo,sans-serif">✗ אינו הדרך הקצרה ביותר (Great Circle)</text>
  <text x="180" y="398" text-anchor="middle" fill="#4a8ac0" font-size="10" font-family="Heebo,sans-serif">Rhumb Line — קו ריים</text>
`,

// Q169: Seasons = 23.5° tilt of Earth's axis
'seasons': `
  <rect width="360" height="420" fill="#050a18"/>
  <circle cx="180" cy="210" r="22" fill="#f39c12" opacity="0.9"/>
  ${[0,45,90,135,180,225,270,315].map(d=>{const rd=d*Math.PI/180;return `<line x1="${180+24*Math.cos(rd)}" y1="${210+24*Math.sin(rd)}" x2="${180+34*Math.cos(rd)}" y2="${210+34*Math.sin(rd)}" stroke="#f39c12" stroke-width="2" opacity="0.6"/>`}).join('')}
  <text x="180" y="214" text-anchor="middle" fill="#000" font-size="10" font-family="Heebo,sans-serif" font-weight="700">שמש</text>
  <circle cx="70" cy="100" r="35" fill="#0d3a6e" stroke="#2a6aae" stroke-width="2"/>
  <line x1="62" y1="65" x2="78" y2="135" stroke="#f39c12" stroke-width="2.5"/>
  <text x="85" y="88" fill="#f39c12" font-size="9" font-family="Heebo,sans-serif">23.5°</text>
  <text x="70" y="158" text-anchor="middle" fill="#f39c12" font-size="9" font-family="Heebo,sans-serif" font-weight="700">קיץ בצפון ☀</text>
  <line x1="70" y1="65" x2="70" y2="135" stroke="#aaa" stroke-width="1" stroke-dasharray="3,2" opacity="0.5"/>
  <circle cx="290" cy="310" r="35" fill="#0d3a6e" stroke="#2a6aae" stroke-width="2"/>
  <line x1="282" y1="275" x2="298" y2="345" stroke="#7eb8f7" stroke-width="2.5"/>
  <text x="305" y="298" fill="#7eb8f7" font-size="9" font-family="Heebo,sans-serif">23.5°</text>
  <text x="290" y="360" text-anchor="middle" fill="#7eb8f7" font-size="9" font-family="Heebo,sans-serif" font-weight="700">חורף בצפון ❄</text>
  <line x1="290" y1="275" x2="290" y2="345" stroke="#aaa" stroke-width="1" stroke-dasharray="3,2" opacity="0.5"/>
  <text x="180" y="395" text-anchor="middle" fill="#aaa" font-size="9.5" font-family="Heebo,sans-serif">ציר כדור הארץ נטוי 23.5° → גורם לעונות השנה</text>
`,

// Q170: Moon position → tides
'tides': `
  <rect width="360" height="420" fill="#050a18"/>
  <circle cx="120" cy="200" r="65" fill="#0d3a6e" stroke="#2a6aae" stroke-width="2"/>
  <text x="120" y="204" text-anchor="middle" fill="#7eb8f7" font-size="10" font-family="Heebo,sans-serif">🌍 כדור הארץ</text>
  <ellipse cx="80" cy="200" rx="20" ry="8" fill="#4a90d9" opacity="0.5"/>
  <ellipse cx="160" cy="200" rx="20" ry="8" fill="#4a90d9" opacity="0.5"/>
  <text x="50" y="204" text-anchor="middle" fill="#4a90d9" font-size="8" font-family="Heebo,sans-serif">גאות</text>
  <text x="185" y="204" text-anchor="middle" fill="#4a90d9" font-size="8" font-family="Heebo,sans-serif">גאות</text>
  <circle cx="300" cy="200" r="28" fill="#bbb" stroke="#888" stroke-width="1.5"/>
  <text x="300" y="204" text-anchor="middle" fill="#555" font-size="10" font-family="Heebo,sans-serif">🌕 ירח</text>
  <line x1="195" y1="200" x2="272" y2="200" stroke="#f39c12" stroke-width="2" stroke-dasharray="4,3"/>
  <text x="235" y="195" text-anchor="middle" fill="#f39c12" font-size="9" font-family="Heebo,sans-serif">משיכה</text>
  <rect x="18" y="298" width="324" height="75" rx="7" fill="#0d1e38" stroke="#4a90d9" stroke-width="1.5"/>
  <text x="180" y="318" text-anchor="middle" fill="#4a90d9" font-size="12" font-family="Heebo,sans-serif" font-weight="900">ירח (ושמש) גורמים לגאות ושפל</text>
  <text x="180" y="336" text-anchor="middle" fill="#fff" font-size="10.5" font-family="Heebo,sans-serif">קו ישר ירח-כדור הארץ-שמש = גאות גדולה (Spring Tide)</text>
  <text x="180" y="354" text-anchor="middle" fill="#7eb8f7" font-size="10" font-family="Heebo,sans-serif">מיקום הירח = מחזור הגאות</text>
  <text x="180" y="398" text-anchor="middle" fill="#4a8ac0" font-size="10" font-family="Heebo,sans-serif">גאות ושפל</text>
`,

// Q165: Latitude lines = parallel small circles
'latitude_lines': `
  <rect width="360" height="420" fill="#080f1a"/>
  <ellipse cx="180" cy="210" rx="130" ry="50" fill="none" stroke="#f39c12" stroke-width="3"/>
  <text x="180" y="268" text-anchor="middle" fill="#f39c12" font-size="9" font-family="Heebo,sans-serif" font-weight="700">קו המשווה — מעגל גדול (0°)</text>
  <ellipse cx="180" cy="165" rx="100" ry="38" fill="none" stroke="#4a90d9" stroke-width="1.8"/>
  <text x="285" y="168" fill="#4a90d9" font-size="8" font-family="Arial">30°N</text>
  <ellipse cx="180" cy="130" rx="65" ry="25" fill="none" stroke="#4a90d9" stroke-width="1.5"/>
  <text x="248" y="133" fill="#4a90d9" font-size="8" font-family="Arial">60°N</text>
  <ellipse cx="180" cy="108" rx="30" ry="11" fill="none" stroke="#7eb8f7" stroke-width="1.2"/>
  <text x="214" y="111" fill="#7eb8f7" font-size="8" font-family="Arial">80°N</text>
  <circle cx="180" cy="98" r="3" fill="white"/>
  <text x="195" y="98" fill="white" font-size="8" font-family="Arial">90°N</text>
  <ellipse cx="180" cy="255" rx="100" ry="38" fill="none" stroke="#4a90d9" stroke-width="1.8"/>
  <text x="285" y="258" fill="#4a90d9" font-size="8" font-family="Arial">30°S</text>
  <rect x="18" y="310" width="324" height="62" rx="7" fill="#0d1e38" stroke="#4a90d9" stroke-width="1.5"/>
  <text x="180" y="330" text-anchor="middle" fill="#4a90d9" font-size="12" font-family="Heebo,sans-serif" font-weight="900">קווי רוחב = מעגלים מקבילים</text>
  <text x="180" y="348" text-anchor="middle" fill="#fff" font-size="10.5" font-family="Heebo,sans-serif">קו המשווה = מעגל גדול; השאר = מעגלים קטנים</text>
  <text x="180" y="364" text-anchor="middle" fill="#7eb8f7" font-size="10" font-family="Heebo,sans-serif">גודלם קטן ככל שמתקרבים לקטב</text>
  <text x="180" y="398" text-anchor="middle" fill="#4a8ac0" font-size="10" font-family="Heebo,sans-serif">קווי רוחב (Parallels)</text>
`,

// Q166: Longitude lines = great circles through both poles
'longitude_lines': `
  <rect width="360" height="420" fill="#080f1a"/>
  <circle cx="180" cy="180" r="120" fill="#0c1828" stroke="#1e3a5a" stroke-width="1.5"/>
  <ellipse cx="180" cy="180" rx="120" ry="40" fill="none" stroke="#f39c12" stroke-width="1.5" opacity="0.5"/>
  ${[0,30,60,90,120,150].map(a=>{const rd=a*Math.PI/180;const x1=180+120*Math.sin(rd),x2=180-120*Math.sin(rd);return `<ellipse cx="180" cy="180" rx="${120*Math.abs(Math.cos(rd))||3}" ry="120" fill="none" stroke="#4a90d9" stroke-width="${a===0?2.5:1.2}" opacity="${a===0?1:0.6}"/>`}).join('')}
  <circle cx="180" cy="60" r="6" fill="white"/>
  <text x="195" y="64" fill="white" font-size="9" font-family="Heebo,sans-serif">קוטב צפוני</text>
  <circle cx="180" cy="300" r="6" fill="white"/>
  <text x="195" y="304" fill="white" font-size="9" font-family="Heebo,sans-serif">קוטב דרומי</text>
  <text x="200" y="183" fill="#f39c12" font-size="10" font-family="Arial" font-weight="700">0° גרינוויץ</text>
  <rect x="18" y="328" width="324" height="50" rx="7" fill="#0d1e38" stroke="#4a90d9" stroke-width="1.5"/>
  <text x="180" y="348" text-anchor="middle" fill="#4a90d9" font-size="12" font-family="Heebo,sans-serif" font-weight="900">קווי אורך = מעגלים גדולים</text>
  <text x="180" y="366" text-anchor="middle" fill="#fff" font-size="10.5" font-family="Heebo,sans-serif">כולם עוברים בשני הקטבים, ניצבים לקו המשווה</text>
  <text x="180" y="398" text-anchor="middle" fill="#4a8ac0" font-size="10" font-family="Heebo,sans-serif">קווי אורך (Meridians)</text>
`,

// Q118: 90 degrees from equator to each pole
'poles_90': `
  <rect width="360" height="420" fill="#080f1a"/>
  <ellipse cx="180" cy="210" rx="120" ry="40" fill="none" stroke="#f39c12" stroke-width="2"/>
  <text x="310" y="214" fill="#f39c12" font-size="10" font-family="Heebo,sans-serif">0° — קו המשווה</text>
  <circle cx="180" cy="70" r="8" fill="white"/>
  <text x="195" y="74" fill="white" font-size="10" font-family="Heebo,sans-serif" font-weight="700">קוטב צפוני — 90°N</text>
  <circle cx="180" cy="350" r="8" fill="white"/>
  <text x="195" y="354" fill="white" font-size="10" font-family="Heebo,sans-serif" font-weight="700">קוטב דרומי — 90°S</text>
  <line x1="180" y1="78" x2="180" y2="205" stroke="#4a90d9" stroke-width="2.5" stroke-dasharray="5,3"/>
  <line x1="180" y1="215" x2="180" y2="342" stroke="#4a90d9" stroke-width="2.5" stroke-dasharray="5,3"/>
  <text x="195" y="148" fill="#4a90d9" font-size="13" font-family="Arial" font-weight="700">90°N</text>
  <text x="195" y="285" fill="#4a90d9" font-size="13" font-family="Arial" font-weight="700">90°S</text>
  <circle cx="180" cy="210" r="5" fill="#f39c12"/>
  <rect x="180" y="60" width="90" height="155" fill="none"/>
  <line x1="160" y1="78" x2="160" y2="205" stroke="#4a90d9" stroke-width="0.7" stroke-dasharray="2,2" opacity="0.4"/>
  <text x="180" y="398" text-anchor="middle" fill="#4a8ac0" font-size="10" font-family="Heebo,sans-serif">קווי רוחב: 0° (קו משווה) עד 90° לכל קוטב</text>
`,

// Q119: Greenwich meridian = 0°, great circle, all true
'greenwich': `
  <rect width="360" height="420" fill="#080f1a"/>
  <circle cx="180" cy="185" r="115" fill="#0c1828" stroke="#1e3a5a" stroke-width="1.5"/>
  <line x1="180" y1="70" x2="180" y2="300" stroke="#f39c12" stroke-width="3"/>
  <text x="180" y="64" text-anchor="middle" fill="#f39c12" font-size="10" font-family="Heebo,sans-serif" font-weight="700">0° — קו גרינוויץ</text>
  <line x1="65" y1="185" x2="295" y2="185" stroke="#1e3a5a" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="310" y="189" fill="#4a6a8a" font-size="8" font-family="Heebo,sans-serif">קו משווה</text>
  <ellipse cx="180" cy="185" rx="115" ry="35" fill="none" stroke="#1e3a5a" stroke-width="1" opacity="0.5"/>
  <circle cx="180" cy="70" r="5" fill="white"/>
  <text x="158" y="315" text-anchor="middle" fill="#f39c12" font-size="9" font-family="Heebo,sans-serif">180°</text>
  <text x="65" y="189" fill="#4a6a8a" font-size="8" font-family="Arial">180°W</text>
  <text x="287" y="189" fill="#4a6a8a" font-size="8" font-family="Arial">180°E</text>
  <circle cx="175" cy="162" r="5" fill="#2ecc71"/>
  <text x="185" y="160" fill="#2ecc71" font-size="8.5" font-family="Heebo,sans-serif">גרינוויץ, לונדון</text>
  <rect x="18" y="328" width="324" height="45" rx="7" fill="#0d1e38" stroke="#f39c12" stroke-width="1.5"/>
  <text x="180" y="346" text-anchor="middle" fill="#f39c12" font-size="11" font-family="Heebo,sans-serif" font-weight="900">קו אורך גרינוויץ = 0° — כל 3 האפשרויות נכונות:</text>
  <text x="180" y="363" text-anchor="middle" fill="#aaa" font-size="10" font-family="Heebo,sans-serif">קו ראשוני | עובר בגרינוויץ | חצי ממעגל גדול (שחציו 180°)</text>
  <text x="180" y="398" text-anchor="middle" fill="#4a8ac0" font-size="10" font-family="Heebo,sans-serif">קו אורך גרינוויץ</text>
`,

});

Object.assign(SCENES_QA, {
'lights_power': `<rect width="360" height="420" fill="#050d1a"/>
<circle cx="35" cy="25" r="1" fill="white" opacity=".7"/><circle cx="310" cy="18" r="1" fill="white" opacity=".6"/><circle cx="75" cy="55" r="1.2" fill="white" opacity=".8"/><circle cx="280" cy="50" r="1" fill="white" opacity=".5"/><circle cx="145" cy="22" r=".8" fill="white" opacity=".7"/>
<path d="M180,155 L111,184 A75,75 0 1,1 249,184 Z" fill="white" opacity=".05"/>
<path d="M180,155 L111,184 A75,75 0 1,1 249,184 Z" fill="none" stroke="white" stroke-width="1" opacity=".25"/>
<path d="M180,155 L222,93 A75,75 0 0,1 222,217 Z" fill="#2ecc71" opacity=".1"/>
<path d="M180,155 L138,217 A75,75 0 0,1 138,93 Z" fill="#e74c3c" opacity=".1"/>
<path d="M180,155 L249,184 A75,75 0 0,1 111,184 Z" fill="white" opacity=".04"/>
<ellipse cx="180" cy="155" rx="20" ry="50" fill="#0d2040" stroke="#2a4a8a" stroke-width="1.5"/>
<polygon points="180,100 169,116 191,116" fill="#2a4a8a"/>
<circle cx="180" cy="115" r="8" fill="white"><animate attributeName="opacity" values="1;.5;1" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="115" r="8" fill="white" opacity=".1"><animate attributeName="r" values="10;22;10" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="200" cy="152" r="6" fill="#2ecc71"><animate attributeName="opacity" values="1;.4;1" dur="2s" begin=".3s" repeatCount="indefinite"/></circle>
<circle cx="200" cy="152" r="6" fill="#2ecc71" opacity=".1"><animate attributeName="r" values="8;18;8" dur="2s" begin=".3s" repeatCount="indefinite"/></circle>
<circle cx="160" cy="152" r="6" fill="#e74c3c"><animate attributeName="opacity" values="1;.4;1" dur="2s" begin=".6s" repeatCount="indefinite"/></circle>
<circle cx="160" cy="152" r="6" fill="#e74c3c" opacity=".1"><animate attributeName="r" values="8;18;8" dur="2s" begin=".6s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="200" r="6" fill="white"><animate attributeName="opacity" values=".9;.4;.9" dur="2s" begin=".9s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="200" r="6" fill="white" opacity=".1"><animate attributeName="r" values="8;16;8" dur="2s" begin=".9s" repeatCount="indefinite"/></circle>
<text x="192" y="112" fill="white" font-size="8" font-family="Heebo,sans-serif">ראש-תורן</text>
<text x="205" y="155" fill="#2ecc71" font-size="8" font-family="Heebo,sans-serif">ירוק</text>
<text x="118" y="155" fill="#e74c3c" font-size="8" font-family="Heebo,sans-serif">אדום</text>
<text x="186" y="216" fill="#ccc" font-size="8" font-family="Heebo,sans-serif">ירכתיים</text>
<text x="180" y="72" text-anchor="middle" fill="#4a6a8a" font-size="8" font-family="Heebo,sans-serif">קדמה ↑</text>
<rect x="18" y="282" width="324" height="115" rx="8" fill="#0d1e38" stroke="#7eb8f7" stroke-width="1.5"/>
<text x="180" y="302" text-anchor="middle" fill="white" font-size="13" font-family="Heebo,sans-serif" font-weight="900">ספינה ממוכנת בדרכה</text>
<text x="180" y="320" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">לבן ראש-תורן (225°) + ירוק + אדום + לבן ירכתיים (135°)</text>
<text x="180" y="337" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">ראש-תורן: קדמה + 112.5° לכל צד — לא נראה מהירכתיים</text>
<text x="180" y="354" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">אורות צד: 112.5° כל אחד | אור ירכתיים: 135° לאחור</text>
<text x="180" y="375" text-anchor="middle" fill="#f39c12" font-size="10" font-family="Heebo,sans-serif" font-weight="700">מעל 50מ' — חייבת שני ראשי-תורן (קדמי נמוך, אחורי גבוה)</text>
`,
'lights_arc_green': `<rect width="360" height="420" fill="#050d1a"/>
<circle cx="35" cy="25" r="1" fill="white" opacity=".7"/><circle cx="310" cy="18" r="1" fill="white" opacity=".6"/><circle cx="75" cy="55" r="1.2" fill="white" opacity=".8"/><circle cx="280" cy="50" r="1" fill="white" opacity=".5"/>
<path d="M180,155 L222,93 A75,75 0 0,1 222,217 Z" fill="#2ecc71" opacity=".15"/>
<path d="M180,155 L222,93 A75,75 0 0,1 222,217 Z" fill="none" stroke="#2ecc71" stroke-width="1.5" opacity=".5"/>
<path d="M180,155 L138,217 A75,75 0 0,1 138,93 Z" fill="#e74c3c" opacity=".15"/>
<path d="M180,155 L138,217 A75,75 0 0,1 138,93 Z" fill="none" stroke="#e74c3c" stroke-width="1.5" opacity=".5"/>
<ellipse cx="180" cy="155" rx="20" ry="50" fill="#0d2040" stroke="#2a4a8a" stroke-width="1.5"/>
<polygon points="180,100 169,116 191,116" fill="#2a4a8a"/>
<circle cx="200" cy="152" r="7" fill="#2ecc71"><animate attributeName="opacity" values="1;.4;1" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="200" cy="152" r="7" fill="#2ecc71" opacity=".1"><animate attributeName="r" values="9;22;9" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="160" cy="152" r="7" fill="#e74c3c"><animate attributeName="opacity" values="1;.4;1" dur="2s" begin=".5s" repeatCount="indefinite"/></circle>
<circle cx="160" cy="152" r="7" fill="#e74c3c" opacity=".1"><animate attributeName="r" values="9;22;9" dur="2s" begin=".5s" repeatCount="indefinite"/></circle>
<text x="248" y="100" fill="#2ecc71" font-size="9" font-family="Heebo,sans-serif" font-weight="700">112.5°</text>
<text x="248" y="115" fill="#2ecc71" font-size="9" font-family="Heebo,sans-serif">ירוק (ימין)</text>
<text x="52" y="100" fill="#e74c3c" font-size="9" font-family="Heebo,sans-serif" font-weight="700">112.5°</text>
<text x="52" y="115" fill="#e74c3c" font-size="9" font-family="Heebo,sans-serif">אדום (שמאל)</text>
<text x="180" y="72" text-anchor="middle" fill="#4a6a8a" font-size="8" font-family="Heebo,sans-serif">קדמה ↑</text>
<rect x="18" y="282" width="324" height="115" rx="8" fill="#0d1e38" stroke="#2ecc71" stroke-width="1.5"/>
<text x="180" y="302" text-anchor="middle" fill="#2ecc71" font-size="13" font-family="Heebo,sans-serif" font-weight="900">קשת אורות הצד — 112.5° כל אחד</text>
<text x="180" y="320" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">ירוק (starboard/ימין): מקדמת ספינה ועד 112.5° ימינה</text>
<text x="180" y="337" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">אדום (port/שמאל): מקדמת ספינה ועד 112.5° שמאלה</text>
<text x="180" y="354" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">שניהם ביחד = 225° | הנותרים 135° = אור ירכתיים לבן</text>
<text x="180" y="375" text-anchor="middle" fill="#f39c12" font-size="10" font-family="Heebo,sans-serif" font-weight="700">אם רואים ירוק בלבד — הספינה ניגשת מימין שלך</text>
`,
'lights_sailing': `<rect width="360" height="420" fill="#050d1a"/>
<circle cx="35" cy="25" r="1" fill="white" opacity=".7"/><circle cx="310" cy="18" r="1" fill="white" opacity=".6"/><circle cx="75" cy="55" r="1.2" fill="white" opacity=".8"/><circle cx="145" cy="22" r=".8" fill="white" opacity=".7"/>
<path d="M180,155 L222,93 A75,75 0 0,1 222,217 Z" fill="#2ecc71" opacity=".08"/>
<path d="M180,155 L138,217 A75,75 0 0,1 138,93 Z" fill="#e74c3c" opacity=".08"/>
<path d="M180,155 L249,184 A75,75 0 0,1 111,184 Z" fill="white" opacity=".04"/>
<ellipse cx="180" cy="155" rx="20" ry="50" fill="#0d2040" stroke="#2a4a8a" stroke-width="1.5"/>
<polygon points="180,100 169,116 191,116" fill="#2a4a8a"/>
<line x1="180" y1="108" x2="180" y2="148" stroke="#4a6a8a" stroke-width="1" stroke-dasharray="3,3"/>
<text x="184" y="120" fill="#4a6a8a" font-size="7.5" font-family="Heebo,sans-serif">ללא ראש-תורן</text>
<circle cx="200" cy="152" r="6" fill="#2ecc71"><animate attributeName="opacity" values="1;.4;1" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="200" cy="152" r="6" fill="#2ecc71" opacity=".1"><animate attributeName="r" values="8;18;8" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="160" cy="152" r="6" fill="#e74c3c"><animate attributeName="opacity" values="1;.4;1" dur="2s" begin=".5s" repeatCount="indefinite"/></circle>
<circle cx="160" cy="152" r="6" fill="#e74c3c" opacity=".1"><animate attributeName="r" values="8;18;8" dur="2s" begin=".5s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="200" r="6" fill="white"><animate attributeName="opacity" values=".9;.4;.9" dur="2s" begin=".8s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="200" r="6" fill="white" opacity=".1"><animate attributeName="r" values="8;16;8" dur="2s" begin=".8s" repeatCount="indefinite"/></circle>
<text x="205" y="155" fill="#2ecc71" font-size="8" font-family="Heebo,sans-serif">ירוק</text>
<text x="118" y="155" fill="#e74c3c" font-size="8" font-family="Heebo,sans-serif">אדום</text>
<text x="186" y="216" fill="#ccc" font-size="8" font-family="Heebo,sans-serif">ירכתיים</text>
<rect x="18" y="282" width="324" height="115" rx="8" fill="#0d1e38" stroke="#3498db" stroke-width="1.5"/>
<text x="180" y="302" text-anchor="middle" fill="#7eb8f7" font-size="13" font-family="Heebo,sans-serif" font-weight="900">מפרשית בדרכה</text>
<text x="180" y="320" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">אורות צד בלבד (ירוק+אדום) + אור ירכתיים לבן</text>
<text x="180" y="337" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">ללא אור ראש-תורן — זה שמבדיל אותה מממוכנת</text>
<text x="180" y="354" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">מפרשית קטנה: יכולה לאחד שלושת האורות לפנס אחד</text>
<text x="180" y="375" text-anchor="middle" fill="#e74c3c" font-size="10" font-family="Heebo,sans-serif" font-weight="700">הדליקה מנוע — חייבת להוסיף ראש-תורן → ממוכנת!</text>
`,
'lights_nuc': `<rect width="360" height="420" fill="#050d1a"/>
<circle cx="35" cy="25" r="1" fill="white" opacity=".7"/><circle cx="310" cy="18" r="1" fill="white" opacity=".6"/><circle cx="75" cy="55" r="1.2" fill="white" opacity=".8"/><circle cx="280" cy="50" r="1" fill="white" opacity=".5"/>
<ellipse cx="180" cy="178" rx="20" ry="50" fill="#0d2040" stroke="#555" stroke-width="1.5"/>
<polygon points="180,123 169,139 191,139" fill="#555"/>
<text x="180" y="83" text-anchor="middle" fill="#e74c3c" font-size="11" font-family="Heebo,sans-serif" font-weight="900">NUC</text>
<circle cx="180" cy="138" r="11" fill="#e74c3c"><animate attributeName="opacity" values="1;.4;1" dur="1.5s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="138" r="11" fill="#e74c3c" opacity=".1"><animate attributeName="r" values="14;28;14" dur="1.5s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="168" r="11" fill="#e74c3c"><animate attributeName="opacity" values="1;.4;1" dur="1.5s" begin=".4s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="168" r="11" fill="#e74c3c" opacity=".1"><animate attributeName="r" values="14;28;14" dur="1.5s" begin=".4s" repeatCount="indefinite"/></circle>
<text x="197" y="142" fill="#e74c3c" font-size="9" font-family="Heebo,sans-serif">אדום 360°</text>
<text x="197" y="172" fill="#e74c3c" font-size="9" font-family="Heebo,sans-serif">אדום 360°</text>
<line x1="158" y1="138" x2="158" y2="168" stroke="#e74c3c" stroke-width="1" opacity=".4" stroke-dasharray="3,2"/>
<text x="72" y="155" fill="#e74c3c" font-size="8" font-family="Heebo,sans-serif">קו אנכי</text>
<rect x="18" y="272" width="324" height="125" rx="8" fill="#0d1e38" stroke="#e74c3c" stroke-width="1.5"/>
<text x="180" y="292" text-anchor="middle" fill="#e74c3c" font-size="13" font-family="Heebo,sans-serif" font-weight="900">כלי שייט ללא שליטה — NUC</text>
<text x="180" y="310" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">שני אורות אדומים עגולים (360°) בקו אנכי</text>
<text x="180" y="327" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">אינה עושה דרכה: רק שני האדומים</text>
<text x="180" y="344" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">עושה דרכה: + אורות צד + אור ירכתיים</text>
<text x="180" y="361" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">ביום: שני כדורים שחורים בקו אנכי</text>
<text x="180" y="382" text-anchor="middle" fill="#f39c12" font-size="10" font-family="Heebo,sans-serif" font-weight="700">כמעט הכל חייב לפנות דרך ל-NUC</text>
`,
'lights_ram': `<rect width="360" height="420" fill="#050d1a"/>
<circle cx="35" cy="25" r="1" fill="white" opacity=".7"/><circle cx="310" cy="18" r="1" fill="white" opacity=".6"/><circle cx="75" cy="55" r="1.2" fill="white" opacity=".8"/>
<ellipse cx="180" cy="185" rx="20" ry="55" fill="#0d2040" stroke="#2a4a8a" stroke-width="1.5"/>
<polygon points="180,125 169,141 191,141" fill="#2a4a8a"/>
<circle cx="180" cy="140" r="10" fill="#e74c3c"><animate attributeName="opacity" values="1;.4;1" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="140" r="10" fill="#e74c3c" opacity=".1"><animate attributeName="r" values="13;26;13" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="168" r="10" fill="white"><animate attributeName="opacity" values="1;.5;1" dur="2s" begin=".3s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="168" r="10" fill="white" opacity=".1"><animate attributeName="r" values="13;26;13" dur="2s" begin=".3s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="196" r="10" fill="#e74c3c"><animate attributeName="opacity" values="1;.4;1" dur="2s" begin=".6s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="196" r="10" fill="#e74c3c" opacity=".1"><animate attributeName="r" values="13;26;13" dur="2s" begin=".6s" repeatCount="indefinite"/></circle>
<text x="196" y="144" fill="#e74c3c" font-size="9" font-family="Heebo,sans-serif">אדום 360°</text>
<text x="196" y="172" fill="#ddd" font-size="9" font-family="Heebo,sans-serif">לבן 360°</text>
<text x="196" y="200" fill="#e74c3c" font-size="9" font-family="Heebo,sans-serif">אדום 360°</text>
<line x1="158" y1="140" x2="158" y2="196" stroke="#e74c3c" stroke-width="1" opacity=".4" stroke-dasharray="3,2"/>
<text x="72" y="170" fill="#e74c3c" font-size="8" font-family="Heebo,sans-serif">קו אנכי</text>
<rect x="18" y="272" width="324" height="125" rx="8" fill="#0d1e38" stroke="#e74c3c" stroke-width="1.5"/>
<text x="180" y="292" text-anchor="middle" fill="#e74c3c" font-size="13" font-family="Heebo,sans-serif" font-weight="900">מוגבל בכושר תמרון — RAM</text>
<text x="180" y="310" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">אדום – לבן – אדום (מלמעלה למטה) | קו אנכי</text>
<text x="180" y="327" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">דוגמאות: סחיפה, הנחת כבלים, פינוי מוקשים</text>
<text x="180" y="344" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">ביום: כדור – ענבל – כדור בקו אנכי</text>
<text x="180" y="361" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">זכאי למעבר מממוכנת; פונה דרך ל-NUC בלבד</text>
<text x="180" y="382" text-anchor="middle" fill="#f39c12" font-size="10" font-family="Heebo,sans-serif" font-weight="700">זכור: אדום-לבן-אדום (לא לבן-אדום-לבן!)</text>
`,
'lights_anchor': `<rect width="360" height="420" fill="#050d1a"/>
<circle cx="35" cy="25" r="1" fill="white" opacity=".7"/><circle cx="310" cy="18" r="1" fill="white" opacity=".6"/><circle cx="75" cy="55" r="1.2" fill="white" opacity=".8"/>
<ellipse cx="180" cy="165" rx="20" ry="50" fill="#0d2040" stroke="#2a4a8a" stroke-width="1.5"/>
<polygon points="180,110 169,126 191,126" fill="#2a4a8a"/>
<circle cx="180" cy="125" r="11" fill="white"><animate attributeName="opacity" values="1;.5;1" dur="2.5s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="125" r="11" fill="white" opacity=".1"><animate attributeName="r" values="14;30;14" dur="2.5s" repeatCount="indefinite"/></circle>
<text x="197" y="129" fill="white" font-size="9" font-family="Heebo,sans-serif">לבן 360°</text>
<line x1="180" y1="215" x2="180" y2="255" stroke="#888" stroke-width="1.5" stroke-dasharray="4,3"/>
<g transform="translate(180,265)"><circle cx="0" cy="0" r="8" fill="none" stroke="#888" stroke-width="2"/><line x1="0" y1="-8" x2="0" y2="8" stroke="#888" stroke-width="2"/><line x1="-10" y1="8" x2="10" y2="8" stroke="#888" stroke-width="2"/></g>
<rect x="18" y="290" width="324" height="110" rx="8" fill="#0d1e38" stroke="#f5f5ff" stroke-width="1.5"/>
<text x="180" y="310" text-anchor="middle" fill="white" font-size="13" font-family="Heebo,sans-serif" font-weight="900">ספינה עוגנת בלילה</text>
<text x="180" y="328" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">אור לבן עגול אחד (360°) בנקודה הנראית ביותר</text>
<text x="180" y="345" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">ספינה מעל 50מ': שניים — ראש (גבוה) + ירכתיים (נמוך)</text>
<text x="180" y="362" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">ביום: כדור שחור אחד (ספינה מעל 7מ')</text>
<text x="180" y="383" text-anchor="middle" fill="#f39c12" font-size="10" font-family="Heebo,sans-serif" font-weight="700">שאלה: אור עוגן = קדמי (לא ירכתיים!)</text>
`,
'lights_aground': `<rect width="360" height="420" fill="#050d1a"/>
<circle cx="35" cy="25" r="1" fill="white" opacity=".7"/><circle cx="310" cy="18" r="1" fill="white" opacity=".6"/><circle cx="75" cy="55" r="1.2" fill="white" opacity=".8"/>
<g transform="rotate(8,180,170)"><ellipse cx="180" cy="170" rx="20" ry="50" fill="#0d2040" stroke="#2a4a8a" stroke-width="1.5"/><polygon points="180,115 169,131 191,131" fill="#2a4a8a"/></g>
<circle cx="180" cy="122" r="8" fill="white"><animate attributeName="opacity" values="1;.5;1" dur="2.5s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="142" r="9" fill="#e74c3c"><animate attributeName="opacity" values="1;.4;1" dur="1.5s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="142" r="9" fill="#e74c3c" opacity=".1"><animate attributeName="r" values="12;24;12" dur="1.5s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="165" r="9" fill="#e74c3c"><animate attributeName="opacity" values="1;.4;1" dur="1.5s" begin=".3s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="165" r="9" fill="#e74c3c" opacity=".1"><animate attributeName="r" values="12;24;12" dur="1.5s" begin=".3s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="188" r="9" fill="#e74c3c"><animate attributeName="opacity" values="1;.4;1" dur="1.5s" begin=".6s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="188" r="9" fill="#e74c3c" opacity=".1"><animate attributeName="r" values="12;24;12" dur="1.5s" begin=".6s" repeatCount="indefinite"/></circle>
<text x="194" y="126" fill="white" font-size="8" font-family="Heebo,sans-serif">לבן (עוגן)</text>
<text x="194" y="146" fill="#e74c3c" font-size="8" font-family="Heebo,sans-serif">אדום</text>
<text x="194" y="169" fill="#e74c3c" font-size="8" font-family="Heebo,sans-serif">אדום</text>
<text x="194" y="192" fill="#e74c3c" font-size="8" font-family="Heebo,sans-serif">אדום</text>
<rect x="18" y="275" width="324" height="120" rx="8" fill="#0d1e38" stroke="#e74c3c" stroke-width="1.5"/>
<text x="180" y="295" text-anchor="middle" fill="#e74c3c" font-size="13" font-family="Heebo,sans-serif" font-weight="900">ספינה על שרטון</text>
<text x="180" y="313" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">אורות עוגן (לבן) + שלושה אדומים עגולים בקו אנכי</text>
<text x="180" y="330" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">שלושת האדומים: נוספים על אורות העוגן, לא מחליפים</text>
<text x="180" y="347" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">ביום: אורות עוגן + שלושה כדורים שחורים</text>
<text x="180" y="368" text-anchor="middle" fill="#f39c12" font-size="10" font-family="Heebo,sans-serif" font-weight="700">שרטון = עוגנת + 3 אדומים | NUC = 2 אדומים בלבד</text>
`,
'lights_large': `<rect width="360" height="420" fill="#050d1a"/>
<circle cx="35" cy="25" r="1" fill="white" opacity=".7"/><circle cx="310" cy="18" r="1" fill="white" opacity=".6"/><circle cx="75" cy="55" r="1.2" fill="white" opacity=".8"/>
<ellipse cx="180" cy="165" rx="20" ry="65" fill="#0d2040" stroke="#2a4a8a" stroke-width="1.5"/>
<polygon points="180,95 169,111 191,111" fill="#2a4a8a"/>
<circle cx="180" cy="110" r="8" fill="white"><animate attributeName="opacity" values="1;.5;1" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="110" r="8" fill="white" opacity=".1"><animate attributeName="r" values="10;22;10" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="133" r="8" fill="white"><animate attributeName="opacity" values="1;.5;1" dur="2s" begin=".5s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="133" r="8" fill="white" opacity=".1"><animate attributeName="r" values="10;22;10" dur="2s" begin=".5s" repeatCount="indefinite"/></circle>
<text x="193" y="114" fill="white" font-size="7.5" font-family="Heebo,sans-serif">ראש-תורן קדמי (נמוך)</text>
<text x="193" y="137" fill="white" font-size="7.5" font-family="Heebo,sans-serif">ראש-תורן אחורי (גבוה)</text>
<line x1="168" y1="110" x2="168" y2="133" stroke="white" stroke-width="0.5" stroke-dasharray="2,2" opacity=".4"/>
<circle cx="200" cy="162" r="6" fill="#2ecc71"><animate attributeName="opacity" values="1;.4;1" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="160" cy="162" r="6" fill="#e74c3c"><animate attributeName="opacity" values="1;.4;1" dur="2s" begin=".5s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="222" r="6" fill="white"><animate attributeName="opacity" values=".9;.4;.9" dur="2s" begin=".9s" repeatCount="indefinite"/></circle>
<rect x="18" y="278" width="324" height="120" rx="8" fill="#0d1e38" stroke="#f5f5ff" stroke-width="1.5"/>
<text x="180" y="298" text-anchor="middle" fill="white" font-size="13" font-family="Heebo,sans-serif" font-weight="900">ספינה ממוכנת מעל 50 מטר</text>
<text x="180" y="316" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">שני אורות ראש-תורן: קדמי (נמוך) + אחורי (גבוה)</text>
<text x="180" y="333" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">+ אורות צד ירוק+אדום + אור ירכתיים לבן</text>
<text x="180" y="350" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">אם רואים שניהם זה מעל זה — ניגשת ישירות אליך</text>
<text x="180" y="371" text-anchor="middle" fill="#f39c12" font-size="10" font-family="Heebo,sans-serif" font-weight="700">מתחת 50מ': ראש-תורן אחד מספיק</text>
`,
'lights_towing': `<rect width="360" height="420" fill="#050d1a"/>
<circle cx="35" cy="25" r="1" fill="white" opacity=".7"/><circle cx="310" cy="18" r="1" fill="white" opacity=".6"/><circle cx="75" cy="55" r="1.2" fill="white" opacity=".8"/>
<ellipse cx="180" cy="165" rx="20" ry="65" fill="#0d2040" stroke="#2a4a8a" stroke-width="1.5"/>
<polygon points="180,95 169,111 191,111" fill="#2a4a8a"/>
<circle cx="180" cy="110" r="7" fill="white"><animate attributeName="opacity" values="1;.5;1" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="128" r="7" fill="white"><animate attributeName="opacity" values="1;.5;1" dur="2s" begin=".3s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="146" r="7" fill="white"><animate attributeName="opacity" values="1;.5;1" dur="2s" begin=".6s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="222" r="7" fill="#f1c40f"><animate attributeName="opacity" values="1;.4;1" dur="2s" begin=".9s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="222" r="7" fill="#f1c40f" opacity=".1"><animate attributeName="r" values="9;20;9" dur="2s" begin=".9s" repeatCount="indefinite"/></circle>
<text x="192" y="114" fill="white" font-size="8" font-family="Heebo,sans-serif">לבן</text>
<text x="192" y="132" fill="white" font-size="8" font-family="Heebo,sans-serif">לבן</text>
<text x="192" y="150" fill="white" font-size="8" font-family="Heebo,sans-serif">לבן (גרר &gt;200מ')</text>
<text x="192" y="226" fill="#f1c40f" font-size="8" font-family="Heebo,sans-serif">צהוב — ירכתיים (135°)</text>
<circle cx="200" cy="168" r="5" fill="#2ecc71"><animate attributeName="opacity" values="1;.4;1" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="160" cy="168" r="5" fill="#e74c3c"><animate attributeName="opacity" values="1;.4;1" dur="2s" begin=".5s" repeatCount="indefinite"/></circle>
<rect x="18" y="272" width="324" height="125" rx="8" fill="#0d1e38" stroke="#f1c40f" stroke-width="1.5"/>
<text x="180" y="292" text-anchor="middle" fill="#f1c40f" font-size="13" font-family="Heebo,sans-serif" font-weight="900">ספינה גוררת</text>
<text x="180" y="310" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">גרר עד 200מ': 2 לבנים ראש-תורן + צהוב + ירוק+אדום</text>
<text x="180" y="327" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">גרר מעל 200מ': 3 לבנים ראש-תורן + צהוב + ירוק+אדום</text>
<text x="180" y="344" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">אור ירכתיים הצהוב מחליף את אור ירכתיים הלבן הרגיל</text>
<text x="180" y="365" text-anchor="middle" fill="#f39c12" font-size="10" font-family="Heebo,sans-serif" font-weight="700">2 לבנים = גרר קצר | 3 לבנים = גרר ארוך (מעל 200מ')</text>
`,
'lights_trawler': `<rect width="360" height="420" fill="#050d1a"/>
<circle cx="35" cy="25" r="1" fill="white" opacity=".7"/><circle cx="310" cy="18" r="1" fill="white" opacity=".6"/><circle cx="75" cy="55" r="1.2" fill="white" opacity=".8"/><circle cx="280" cy="50" r="1" fill="white" opacity=".5"/><circle cx="145" cy="22" r=".8" fill="white" opacity=".7"/>
<ellipse cx="180" cy="165" rx="20" ry="50" fill="#0d2040" stroke="#2a4a8a" stroke-width="1.5"/>
<polygon points="180,110 169,126 191,126" fill="#2a4a8a"/>
<circle cx="180" cy="135" r="13" fill="#2ecc71"><animate attributeName="opacity" values="1;.4;1" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="135" r="13" fill="#2ecc71" opacity=".1"><animate attributeName="r" values="16;34;16" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="165" r="13" fill="white"><animate attributeName="opacity" values="1;.5;1" dur="2s" begin=".4s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="165" r="13" fill="white" opacity=".1"><animate attributeName="r" values="16;34;16" dur="2s" begin=".4s" repeatCount="indefinite"/></circle>
<text x="200" y="139" fill="#2ecc71" font-size="10" font-family="Heebo,sans-serif" font-weight="700">ירוק 360°</text>
<text x="200" y="169" fill="#e0e0ff" font-size="10" font-family="Heebo,sans-serif" font-weight="700">לבן 360°</text>
<line x1="158" y1="135" x2="158" y2="165" stroke="#2ecc71" stroke-width="1" opacity=".5" stroke-dasharray="3,2"/>
<text x="88" y="152" fill="#2ecc71" font-size="8.5" font-family="Heebo,sans-serif">ירוק מעל</text>
<text x="90" y="162" fill="#2ecc71" font-size="8.5" font-family="Heebo,sans-serif">לבן</text>
<text x="180" y="80" text-anchor="middle" fill="#2ecc71" font-size="10" font-family="Heebo,sans-serif" font-weight="700">טרולר — TRAWLING</text>
<rect x="18" y="282" width="324" height="115" rx="8" fill="#0d1e38" stroke="#2ecc71" stroke-width="1.5"/>
<text x="180" y="302" text-anchor="middle" fill="#2ecc71" font-size="13" font-family="Heebo,sans-serif" font-weight="900">כלי דייג בגרירה (טרולר)</text>
<text x="180" y="320" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">ירוק מעל לבן — שניהם עגולים 360°</text>
<text x="180" y="337" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">אם עושה דרכה: + אורות צד + אור ירכתיים</text>
<text x="180" y="354" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">השווה: דייג שאינו גורר = אדום מעל לבן</text>
<text x="180" y="375" text-anchor="middle" fill="#f39c12" font-size="10" font-family="Heebo,sans-serif" font-weight="700">זכור: ירוק (גרירה) מעל לבן — לא הפוך!</text>
`,
'lights_pilot': `<rect width="360" height="420" fill="#050d1a"/>
<circle cx="35" cy="25" r="1" fill="white" opacity=".7"/><circle cx="310" cy="18" r="1" fill="white" opacity=".6"/><circle cx="75" cy="55" r="1.2" fill="white" opacity=".8"/>
<ellipse cx="180" cy="175" rx="20" ry="50" fill="#0d2040" stroke="#2a4a8a" stroke-width="1.5"/>
<polygon points="180,120 169,136 191,136" fill="#2a4a8a"/>
<circle cx="180" cy="148" r="12" fill="white"><animate attributeName="opacity" values="1;.5;1" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="148" r="12" fill="white" opacity=".1"><animate attributeName="r" values="15;28;15" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="178" r="12" fill="#e74c3c"><animate attributeName="opacity" values="1;.4;1" dur="2s" begin=".5s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="178" r="12" fill="#e74c3c" opacity=".1"><animate attributeName="r" values="15;28;15" dur="2s" begin=".5s" repeatCount="indefinite"/></circle>
<text x="198" y="152" fill="white" font-size="10" font-family="Heebo,sans-serif" font-weight="700">לבן 360°</text>
<text x="198" y="182" fill="#e74c3c" font-size="10" font-family="Heebo,sans-serif" font-weight="700">אדום 360°</text>
<line x1="158" y1="148" x2="158" y2="178" stroke="white" stroke-width="1" opacity=".3" stroke-dasharray="3,2"/>
<rect x="18" y="278" width="324" height="120" rx="8" fill="#0d1e38" stroke="#ddd" stroke-width="1.5"/>
<text x="180" y="298" text-anchor="middle" fill="white" font-size="13" font-family="Heebo,sans-serif" font-weight="900">ספינת פיילוט בשירות</text>
<text x="180" y="316" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">לבן מעל אדום — שניהם עגולים 360°</text>
<text x="180" y="333" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">בנוסף אם בדרכה: + אורות צד + ירכתיים</text>
<text x="180" y="350" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">השווה: דייג לא-גורר = אדום מעל לבן (הפוך!)</text>
<text x="180" y="371" text-anchor="middle" fill="#f39c12" font-size="10" font-family="Heebo,sans-serif" font-weight="700">פיילוט: לבן למעלה | דייג לא-גורר: אדום למעלה</text>
`,
'lights_minesweeper': `<rect width="360" height="420" fill="#050d1a"/>
<circle cx="35" cy="25" r="1" fill="white" opacity=".7"/><circle cx="310" cy="18" r="1" fill="white" opacity=".6"/><circle cx="75" cy="55" r="1.2" fill="white" opacity=".8"/>
<ellipse cx="180" cy="180" rx="25" ry="50" fill="#0d2040" stroke="#2a4a8a" stroke-width="1.5"/>
<polygon points="180,125 169,141 191,141" fill="#2a4a8a"/>
<line x1="155" y1="178" x2="88" y2="178" stroke="#333" stroke-width="2"/>
<line x1="205" y1="178" x2="272" y2="178" stroke="#333" stroke-width="2"/>
<circle cx="180" cy="135" r="9" fill="#2ecc71"><animate attributeName="opacity" values="1;.4;1" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="135" r="9" fill="#2ecc71" opacity=".1"><animate attributeName="r" values="12;26;12" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="88" cy="178" r="9" fill="#2ecc71"><animate attributeName="opacity" values="1;.4;1" dur="2s" begin=".4s" repeatCount="indefinite"/></circle>
<circle cx="88" cy="178" r="9" fill="#2ecc71" opacity=".1"><animate attributeName="r" values="12;26;12" dur="2s" begin=".4s" repeatCount="indefinite"/></circle>
<circle cx="272" cy="178" r="9" fill="#2ecc71"><animate attributeName="opacity" values="1;.4;1" dur="2s" begin=".8s" repeatCount="indefinite"/></circle>
<circle cx="272" cy="178" r="9" fill="#2ecc71" opacity=".1"><animate attributeName="r" values="12;26;12" dur="2s" begin=".8s" repeatCount="indefinite"/></circle>
<text x="186" y="139" fill="#2ecc71" font-size="8" font-family="Heebo,sans-serif">ראש-תורן</text>
<text x="22" y="196" fill="#2ecc71" font-size="8" font-family="Heebo,sans-serif">קצה שמאל</text>
<text x="238" y="196" fill="#2ecc71" font-size="8" font-family="Heebo,sans-serif">קצה ימין</text>
<rect x="18" y="272" width="324" height="125" rx="8" fill="#0d1e38" stroke="#2ecc71" stroke-width="1.5"/>
<text x="180" y="292" text-anchor="middle" fill="#2ecc71" font-size="13" font-family="Heebo,sans-serif" font-weight="900">ספינת סופות (מינסוויפר)</text>
<text x="180" y="310" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">שלושה אורות ירוקים עגולים (360°)</text>
<text x="180" y="327" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">1 בראש-תורן + 1 בכל קצה קורת הסיפון הרוחבית</text>
<text x="180" y="344" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">+ אורות ניווט רגילים (ממוכנת + RAM)</text>
<text x="180" y="365" text-anchor="middle" fill="#e74c3c" font-size="10" font-family="Heebo,sans-serif" font-weight="700">אזהרה: אל תתקרב ל-1000 מטר ממינסוויפר!</text>
`,
'lights_stern': `<rect width="360" height="420" fill="#050d1a"/>
<circle cx="35" cy="25" r="1" fill="white" opacity=".7"/><circle cx="310" cy="18" r="1" fill="white" opacity=".6"/><circle cx="75" cy="55" r="1.2" fill="white" opacity=".8"/>
<path d="M180,155 L249,184 A75,75 0 0,1 111,184 Z" fill="white" opacity=".12"/>
<path d="M180,155 L249,184 A75,75 0 0,1 111,184 Z" fill="none" stroke="white" stroke-width="1.5" opacity=".4"/>
<ellipse cx="180" cy="145" rx="20" ry="50" fill="#0d2040" stroke="#2a4a8a" stroke-width="1.5"/>
<polygon points="180,90 169,106 191,106" fill="#2a4a8a"/>
<circle cx="180" cy="190" r="9" fill="white"><animate attributeName="opacity" values="1;.5;1" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="190" r="9" fill="white" opacity=".1"><animate attributeName="r" values="12;25;12" dur="2s" repeatCount="indefinite"/></circle>
<text x="186" y="208" fill="white" font-size="9" font-family="Heebo,sans-serif">לבן ירכתיים</text>
<text x="112" y="200" fill="#4a6a8a" font-size="8" font-family="Heebo,sans-serif">67.5°</text>
<text x="232" y="200" fill="#4a6a8a" font-size="8" font-family="Heebo,sans-serif">67.5°</text>
<text x="180" y="225" text-anchor="middle" fill="#7eb8f7" font-size="9" font-family="Heebo,sans-serif">← 135° →</text>
<rect x="18" y="272" width="324" height="125" rx="8" fill="#0d1e38" stroke="#ddd" stroke-width="1.5"/>
<text x="180" y="292" text-anchor="middle" fill="white" font-size="13" font-family="Heebo,sans-serif" font-weight="900">אור ירכתיים (Stern Light)</text>
<text x="180" y="310" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">צבע: לבן | קשת: 135° לאחור</text>
<text x="180" y="327" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">67.5° מכל צד מאחורי הספינה</text>
<text x="180" y="344" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">ראש-תורן (225°) + ירכתיים (135°) = 360° כיסוי מלא</text>
<text x="180" y="365" text-anchor="middle" fill="#f39c12" font-size="10" font-family="Heebo,sans-serif" font-weight="700">רואים רק לבן אחד? — הספינה מתרחקת ממך</text>
`,
'lights_small': `<rect width="360" height="420" fill="#050d1a"/>
<circle cx="35" cy="25" r="1" fill="white" opacity=".7"/><circle cx="310" cy="18" r="1" fill="white" opacity=".6"/><circle cx="75" cy="55" r="1.2" fill="white" opacity=".8"/>
<ellipse cx="180" cy="175" rx="12" ry="32" fill="#0d2040" stroke="#2a4a8a" stroke-width="1.5"/>
<polygon points="180,138 173,150 187,150" fill="#2a4a8a"/>
<circle cx="180" cy="158" r="13" fill="white"><animate attributeName="opacity" values="1;.5;1" dur="2.5s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="158" r="13" fill="white" opacity=".1"><animate attributeName="r" values="16;36;16" dur="2.5s" repeatCount="indefinite"/></circle>
<text x="200" y="162" fill="white" font-size="10" font-family="Heebo,sans-serif" font-weight="700">לבן 360°</text>
<text x="180" y="220" text-anchor="middle" fill="#4a6a8a" font-size="9" font-family="Heebo,sans-serif">סירה קטנה (מתחת 7מ')</text>
<rect x="18" y="280" width="324" height="118" rx="8" fill="#0d1e38" stroke="#ddd" stroke-width="1.5"/>
<text x="180" y="300" text-anchor="middle" fill="white" font-size="13" font-family="Heebo,sans-serif" font-weight="900">כלי שייט מתחת ל-7 מטר</text>
<text x="180" y="318" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">אור לבן עגול אחד — נראה מכל הכיוונים</text>
<text x="180" y="335" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">בתנאי: מהירות מקסימלית 7 קשרים</text>
<text x="180" y="352" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">מהיר יותר: חייבת אורות צד + ירכתיים כמו כולם</text>
<text x="180" y="373" text-anchor="middle" fill="#f39c12" font-size="10" font-family="Heebo,sans-serif" font-weight="700">חרום: פנס ידני מותר — הכן מראש!</text>
`,
'lights_constrained': `<rect width="360" height="420" fill="#050d1a"/>
<circle cx="35" cy="25" r="1" fill="white" opacity=".7"/><circle cx="310" cy="18" r="1" fill="white" opacity=".6"/><circle cx="75" cy="55" r="1.2" fill="white" opacity=".8"/>
<ellipse cx="180" cy="188" rx="20" ry="65" fill="#0d2040" stroke="#2a4a8a" stroke-width="1.5"/>
<polygon points="180,118 169,134 191,134" fill="#2a4a8a"/>
<circle cx="180" cy="136" r="10" fill="#e74c3c"><animate attributeName="opacity" values="1;.4;1" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="136" r="10" fill="#e74c3c" opacity=".1"><animate attributeName="r" values="13;26;13" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="163" r="10" fill="#e74c3c"><animate attributeName="opacity" values="1;.4;1" dur="2s" begin=".35s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="163" r="10" fill="#e74c3c" opacity=".1"><animate attributeName="r" values="13;26;13" dur="2s" begin=".35s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="190" r="10" fill="#e74c3c"><animate attributeName="opacity" values="1;.4;1" dur="2s" begin=".7s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="190" r="10" fill="#e74c3c" opacity=".1"><animate attributeName="r" values="13;26;13" dur="2s" begin=".7s" repeatCount="indefinite"/></circle>
<text x="196" y="140" fill="#e74c3c" font-size="9" font-family="Heebo,sans-serif">אדום 360°</text>
<text x="196" y="167" fill="#e74c3c" font-size="9" font-family="Heebo,sans-serif">אדום 360°</text>
<text x="196" y="194" fill="#e74c3c" font-size="9" font-family="Heebo,sans-serif">אדום 360°</text>
<line x1="158" y1="136" x2="158" y2="190" stroke="#e74c3c" stroke-width="1" opacity=".4" stroke-dasharray="3,2"/>
<rect x="18" y="268" width="324" height="132" rx="8" fill="#0d1e38" stroke="#e74c3c" stroke-width="1.5"/>
<text x="180" y="288" text-anchor="middle" fill="#e74c3c" font-size="12" font-family="Heebo,sans-serif" font-weight="900">מוגבל בשוקע (Constrained by Draft)</text>
<text x="180" y="306" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">שלושה אורות אדומים עגולים בקו אנכי</text>
<text x="180" y="323" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">ביום: גליל שחור</text>
<text x="180" y="340" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">היררכיה: גבוה מממוכן, נמוך מ-RAM ו-NUC</text>
<text x="180" y="357" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">שרטון = עוגן + 3 אדומים | CBD = 3 אדומים בלבד</text>
<text x="180" y="378" text-anchor="middle" fill="#f39c12" font-size="10" font-family="Heebo,sans-serif" font-weight="700">3 אדומים (לא 2!) ללא אור עוגן</text>
`,
'lights_masthead_225': `<rect width="360" height="420" fill="#050d1a"/>
<circle cx="35" cy="25" r="1" fill="white" opacity=".7"/><circle cx="310" cy="18" r="1" fill="white" opacity=".6"/><circle cx="75" cy="55" r="1.2" fill="white" opacity=".8"/>
<path d="M180,165 L111,194 A75,75 0 1,1 249,194 Z" fill="white" opacity=".1"/>
<path d="M180,165 L111,194 A75,75 0 1,1 249,194 Z" fill="none" stroke="white" stroke-width="2" opacity=".4"/>
<line x1="180" y1="88" x2="180" y2="165" stroke="#4a6a8a" stroke-width="1" stroke-dasharray="4,3" opacity=".5"/>
<text x="183" y="82" fill="#4a6a8a" font-size="8" font-family="Heebo,sans-serif">קדמה ↑</text>
<path d="M180,165 L111,194" stroke="#e74c3c" stroke-width="1.5" opacity=".6"/>
<path d="M180,165 L249,194" stroke="#e74c3c" stroke-width="1.5" opacity=".6"/>
<text x="88" y="210" fill="#e74c3c" font-size="8" font-family="Heebo,sans-serif">112.5°</text>
<text x="242" y="210" fill="#e74c3c" font-size="8" font-family="Heebo,sans-serif">112.5°</text>
<text x="180" y="143" text-anchor="middle" fill="white" font-size="11" font-family="Heebo,sans-serif" font-weight="700">225°</text>
<ellipse cx="180" cy="165" rx="20" ry="50" fill="#0d2040" stroke="#2a4a8a" stroke-width="1.5"/>
<polygon points="180,110 169,126 191,126" fill="#2a4a8a"/>
<circle cx="180" cy="128" r="9" fill="white"><animate attributeName="opacity" values="1;.5;1" dur="2s" repeatCount="indefinite"/></circle>
<rect x="18" y="270" width="324" height="128" rx="8" fill="#0d1e38" stroke="#ddd" stroke-width="1.5"/>
<text x="180" y="290" text-anchor="middle" fill="white" font-size="13" font-family="Heebo,sans-serif" font-weight="900">ראש-תורן — קשת 225° מלפנים</text>
<text x="180" y="308" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">112.5° לצד ימין + 112.5° לצד שמאל מהקדמה</text>
<text x="180" y="325" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">הירכתיים (135°) לא מכוסה — שם מציגים אור ירכתיים לבן</text>
<text x="180" y="342" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">ראש-תורן (225°) + ירכתיים (135°) = 360° כיסוי מלא</text>
<text x="180" y="363" text-anchor="middle" fill="#f39c12" font-size="10" font-family="Heebo,sans-serif" font-weight="700">טווח נראות: 3 מיל (50-12מ') | 5 מיל (מעל 50מ')</text>
`,
'lights_visibility': `<rect width="360" height="420" fill="#050d1a"/>
<circle cx="35" cy="25" r="1" fill="white" opacity=".7"/><circle cx="310" cy="18" r="1" fill="white" opacity=".6"/>
<text x="180" y="55" text-anchor="middle" fill="#7eb8f7" font-size="14" font-family="Heebo,sans-serif" font-weight="900">טווחי נראות — COLREGS</text>
<rect x="20" y="68" width="320" height="22" rx="4" fill="#0d2040"/>
<text x="30" y="83" fill="#888" font-size="9" font-family="Heebo,sans-serif">גודל ספינה</text>
<text x="152" y="83" fill="#888" font-size="9" font-family="Heebo,sans-serif">ראש-תורן</text>
<text x="228" y="83" fill="#888" font-size="9" font-family="Heebo,sans-serif">אורות צד</text>
<text x="298" y="83" fill="#888" font-size="9" font-family="Heebo,sans-serif">אור ירכתיים</text>
<rect x="20" y="90" width="320" height="28" rx="0" fill="#091528"/>
<text x="30" y="109" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">מתחת 12 מטר</text>
<text x="162" y="109" fill="white" font-size="10" font-family="Heebo,sans-serif" font-weight="700">2 מיל</text>
<text x="236" y="109" fill="white" font-size="10" font-family="Heebo,sans-serif" font-weight="700">1 מיל</text>
<text x="304" y="109" fill="white" font-size="10" font-family="Heebo,sans-serif" font-weight="700">2 מיל</text>
<rect x="20" y="118" width="320" height="28" rx="0" fill="#0d1e38"/>
<text x="30" y="137" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">12 עד 50 מטר</text>
<text x="162" y="137" fill="#f39c12" font-size="10" font-family="Heebo,sans-serif" font-weight="700">3 מיל</text>
<text x="236" y="137" fill="white" font-size="10" font-family="Heebo,sans-serif" font-weight="700">2 מיל</text>
<text x="304" y="137" fill="white" font-size="10" font-family="Heebo,sans-serif" font-weight="700">2 מיל</text>
<rect x="20" y="146" width="320" height="28" rx="0" fill="#091528"/>
<text x="30" y="165" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">מעל 50 מטר</text>
<text x="162" y="165" fill="#2ecc71" font-size="10" font-family="Heebo,sans-serif" font-weight="700">5 מיל</text>
<text x="236" y="165" fill="white" font-size="10" font-family="Heebo,sans-serif" font-weight="700">3 מיל</text>
<text x="304" y="165" fill="white" font-size="10" font-family="Heebo,sans-serif" font-weight="700">3 מיל</text>
<rect x="20" y="174" width="320" height="22" rx="0" fill="#0d2040"/>
<text x="30" y="189" fill="#aac4e8" font-size="9" font-family="Heebo,sans-serif">אור עוגן (עוגנת)</text>
<text x="152" y="189" fill="white" font-size="9" font-family="Heebo,sans-serif">2 מיל (&lt;50מ') | 3 מיל (&gt;50מ')</text>
<rect x="18" y="215" width="324" height="185" rx="8" fill="#0d1e38" stroke="#f39c12" stroke-width="1.5"/>
<text x="180" y="237" text-anchor="middle" fill="#f39c12" font-size="13" font-family="Heebo,sans-serif" font-weight="900">ספינה 20 מטר = 12–50מ'</text>
<text x="180" y="258" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">ראש-תורן: 3 מיל</text>
<text x="180" y="275" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">אורות צד: 2 מיל | אור ירכתיים: 2 מיל</text>
<text x="180" y="310" text-anchor="middle" fill="#f39c12" font-size="10" font-family="Heebo,sans-serif" font-weight="700">12–50מ' = ראש-תורן 3 מיל | מעל 50מ' = 5 מיל</text>
`,
'lights_when': `<rect width="360" height="420" fill="#050d1a"/>
<defs><linearGradient id="skyG" x1="0" x2="1"><stop offset="0%" stop-color="#050d1a"/><stop offset="38%" stop-color="#0d2040"/><stop offset="50%" stop-color="#c0680a" stop-opacity=".35"/><stop offset="62%" stop-color="#0d2040"/><stop offset="100%" stop-color="#050d1a"/></linearGradient></defs>
<rect x="0" y="55" width="360" height="90" fill="url(#skyG)"/>
<circle cx="50" cy="105" r="20" fill="#0d1e38" stroke="#555" stroke-width="2"/>
<text x="50" y="112" text-anchor="middle" fill="#888" font-size="20">☽</text>
<circle cx="180" cy="98" r="22" fill="#f39c12" opacity=".85"><animate attributeName="opacity" values=".85;.6;.85" dur="4s" repeatCount="indefinite"/></circle>
<text x="180" y="105" text-anchor="middle" fill="white" font-size="16">☀</text>
<circle cx="310" cy="105" r="20" fill="#0d1e38" stroke="#555" stroke-width="2"/>
<text x="310" y="112" text-anchor="middle" fill="#888" font-size="20">☽</text>
<text x="50" y="145" text-anchor="middle" fill="#7eb8f7" font-size="9" font-family="Heebo,sans-serif">שקיעה</text>
<text x="180" y="148" text-anchor="middle" fill="#f39c12" font-size="9" font-family="Heebo,sans-serif">לילה</text>
<text x="310" y="145" text-anchor="middle" fill="#7eb8f7" font-size="9" font-family="Heebo,sans-serif">זריחה</text>
<line x1="50" y1="155" x2="310" y2="155" stroke="#7eb8f7" stroke-width="1.5" stroke-dasharray="5,3"/>
<text x="180" y="172" text-anchor="middle" fill="white" font-size="11" font-family="Heebo,sans-serif" font-weight="700">⬅ חובת אורות ➡</text>
<circle cx="35" cy="22" r="1" fill="white" opacity=".7"/><circle cx="310" cy="18" r="1" fill="white" opacity=".6"/><circle cx="75" cy="32" r="1.2" fill="white" opacity=".8"/><circle cx="145" cy="22" r=".8" fill="white" opacity=".7"/>
<rect x="18" y="188" width="324" height="52" rx="8" fill="#1a3a1a" stroke="#2ecc71" stroke-width="1.5"/>
<text x="180" y="208" text-anchor="middle" fill="#2ecc71" font-size="11" font-family="Heebo,sans-serif" font-weight="900">גם ביום — ראות מוגבלת = חובת אורות!</text>
<text x="180" y="228" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">ערפל, גשם עז, ראות מוגבלת → הדלק אורות</text>
<rect x="18" y="252" width="324" height="148" rx="8" fill="#0d1e38" stroke="#7eb8f7" stroke-width="1.5"/>
<text x="180" y="272" text-anchor="middle" fill="#7eb8f7" font-size="13" font-family="Heebo,sans-serif" font-weight="900">מתי חובת הדלקת אורות?</text>
<text x="180" y="292" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">משקיעת השמש ועד זריחתה</text>
<text x="180" y="310" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">ובכל עת שהראות מוגבלת</text>
<text x="180" y="328" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">(ערפל, גשם, עשן, ראות פחות ממספר מילין)</text>
<text x="180" y="350" text-anchor="middle" fill="#f39c12" font-size="10" font-family="Heebo,sans-serif" font-weight="700">מספיק קרוב לשקיעה? — הדלק עכשיו!</text>
`,
'lights_see_green': `<rect width="360" height="420" fill="#050d1a"/>
<circle cx="35" cy="25" r="1" fill="white" opacity=".7"/><circle cx="310" cy="18" r="1" fill="white" opacity=".6"/><circle cx="75" cy="55" r="1.2" fill="white" opacity=".8"/>
<text x="180" y="45" text-anchor="middle" fill="#4a6a8a" font-size="9" font-family="Heebo,sans-serif">ספינה אחרת</text>
<ellipse cx="258" cy="108" rx="14" ry="35" fill="#0d2040" stroke="#2a4a8a" stroke-width="1.5"/>
<polygon points="258,70 250,82 266,82" fill="#2a4a8a"/>
<circle cx="273" cy="105" r="8" fill="#2ecc71"><animate attributeName="opacity" values="1;.4;1" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="273" cy="105" r="8" fill="#2ecc71" opacity=".1"><animate attributeName="r" values="10;22;10" dur="2s" repeatCount="indefinite"/></circle>
<text x="286" y="109" fill="#2ecc71" font-size="9" font-family="Heebo,sans-serif">ירוק</text>
<text x="228" y="152" fill="#4a6a8a" font-size="7.5" font-family="Heebo,sans-serif">(אדום בצד השני, לא נראה)</text>
<defs><marker id="arr2" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#7eb8f7"/></marker></defs>
<line x1="248" y1="128" x2="180" y2="200" stroke="#7eb8f7" stroke-width="1.5" stroke-dasharray="6,3" marker-end="url(#arr2)"/>
<text x="220" y="185" fill="#7eb8f7" font-size="8" font-family="Heebo,sans-serif">נתיב תנועה</text>
<text x="180" y="222" text-anchor="middle" fill="#4a6a8a" font-size="9" font-family="Heebo,sans-serif">אתה</text>
<ellipse cx="180" cy="248" rx="14" ry="35" fill="#1a3060" stroke="#3a5a9a" stroke-width="1.5"/>
<polygon points="180,210 172,222 188,222" fill="#3a5a9a"/>
<rect x="18" y="295" width="324" height="108" rx="8" fill="#0d1e38" stroke="#2ecc71" stroke-width="1.5"/>
<text x="180" y="315" text-anchor="middle" fill="#2ecc71" font-size="13" font-family="Heebo,sans-serif" font-weight="900">רואים ירוק בלבד?</text>
<text x="180" y="333" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">צד ימין (starboard) שלה פונה אליך</text>
<text x="180" y="350" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">הספינה מגיעה מכיוון ימין שלך</text>
<text x="180" y="371" text-anchor="middle" fill="#f39c12" font-size="10" font-family="Heebo,sans-serif" font-weight="700">ירוק = ימין שלה = היא ניגשת מימינך</text>
`,
'lights_two_whites': `<rect width="360" height="420" fill="#050d1a"/>
<circle cx="35" cy="25" r="1" fill="white" opacity=".7"/><circle cx="310" cy="18" r="1" fill="white" opacity=".6"/><circle cx="75" cy="55" r="1.2" fill="white" opacity=".8"/>
<text x="180" y="48" text-anchor="middle" fill="#4a6a8a" font-size="9" font-family="Heebo,sans-serif">מה רואים מלפנים (head-on)</text>
<ellipse cx="180" cy="152" rx="22" ry="60" fill="#0d2040" stroke="#2a4a8a" stroke-width="1.5"/>
<polygon points="180,87 169,103 191,103" fill="#2a4a8a"/>
<circle cx="180" cy="102" r="9" fill="white"><animate attributeName="opacity" values="1;.5;1" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="102" r="9" fill="white" opacity=".1"><animate attributeName="r" values="11;24;11" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="125" r="9" fill="white"><animate attributeName="opacity" values="1;.5;1" dur="2s" begin=".5s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="125" r="9" fill="white" opacity=".1"><animate attributeName="r" values="11;24;11" dur="2s" begin=".5s" repeatCount="indefinite"/></circle>
<circle cx="202" cy="152" r="6" fill="#2ecc71"><animate attributeName="opacity" values="1;.4;1" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="158" cy="152" r="6" fill="#e74c3c"><animate attributeName="opacity" values="1;.4;1" dur="2s" begin=".5s" repeatCount="indefinite"/></circle>
<text x="196" y="106" fill="white" font-size="7.5" font-family="Heebo,sans-serif">לבן קדמי (נמוך)</text>
<text x="196" y="129" fill="white" font-size="7.5" font-family="Heebo,sans-serif">לבן אחורי (גבוה)</text>
<text x="208" y="156" fill="#2ecc71" font-size="8" font-family="Heebo,sans-serif">ירוק</text>
<text x="120" y="156" fill="#e74c3c" font-size="8" font-family="Heebo,sans-serif">אדום</text>
<rect x="18" y="262" width="324" height="140" rx="8" fill="#0d1e38" stroke="#ddd" stroke-width="1.5"/>
<text x="180" y="282" text-anchor="middle" fill="white" font-size="13" font-family="Heebo,sans-serif" font-weight="900">שני לבנים אחד מעל השני</text>
<text x="180" y="300" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">= שני ראשי-תורן: ספינה ממוכנת מעל 50 מטר</text>
<text x="180" y="317" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">ניגשת אליך מלפנים (head-on)</text>
<text x="180" y="334" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">לבן + ירוק: היא ממולך מעט ימין</text>
<text x="180" y="351" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">לבן + אדום: היא ממולך מעט שמאל</text>
<text x="180" y="372" text-anchor="middle" fill="#f39c12" font-size="10" font-family="Heebo,sans-serif" font-weight="700">שני לבנים זה מעל זה = ספינה גדולה מגיעה!</text>
`,
'lights_red_over_white': `<rect width="360" height="420" fill="#050d1a"/>
<circle cx="35" cy="25" r="1" fill="white" opacity=".7"/><circle cx="310" cy="18" r="1" fill="white" opacity=".6"/><circle cx="75" cy="55" r="1.2" fill="white" opacity=".8"/>
<ellipse cx="180" cy="175" rx="20" ry="50" fill="#0d2040" stroke="#2a4a8a" stroke-width="1.5"/>
<polygon points="180,120 169,136 191,136" fill="#2a4a8a"/>
<circle cx="180" cy="148" r="12" fill="#e74c3c"><animate attributeName="opacity" values="1;.4;1" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="148" r="12" fill="#e74c3c" opacity=".1"><animate attributeName="r" values="15;28;15" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="178" r="12" fill="white"><animate attributeName="opacity" values="1;.5;1" dur="2s" begin=".5s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="178" r="12" fill="white" opacity=".1"><animate attributeName="r" values="15;28;15" dur="2s" begin=".5s" repeatCount="indefinite"/></circle>
<text x="198" y="152" fill="#e74c3c" font-size="10" font-family="Heebo,sans-serif" font-weight="700">אדום 360°</text>
<text x="198" y="182" fill="#ddd" font-size="10" font-family="Heebo,sans-serif" font-weight="700">לבן 360°</text>
<rect x="18" y="278" width="324" height="120" rx="8" fill="#0d1e38" stroke="#e74c3c" stroke-width="1.5"/>
<text x="180" y="298" text-anchor="middle" fill="#e74c3c" font-size="13" font-family="Heebo,sans-serif" font-weight="900">כלי דייג שאינו גורר</text>
<text x="180" y="316" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">אדום מעל לבן — שניהם עגולים 360°</text>
<text x="180" y="333" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">בדרכה: + אורות צד + אור ירכתיים</text>
<text x="180" y="350" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">השווה: טרולר = ירוק מעל לבן | פיילוט = לבן מעל אדום</text>
<text x="180" y="371" text-anchor="middle" fill="#f39c12" font-size="10" font-family="Heebo,sans-serif" font-weight="700">דייג לא-גורר: אדום למעלה | טרולר: ירוק למעלה</text>
`,
'lights_nuc_making_way': `<rect width="360" height="420" fill="#050d1a"/>
<circle cx="35" cy="25" r="1" fill="white" opacity=".7"/><circle cx="310" cy="18" r="1" fill="white" opacity=".6"/><circle cx="75" cy="55" r="1.2" fill="white" opacity=".8"/>
<path d="M180,182 L222,120 A75,75 0 0,1 222,244 Z" fill="#2ecc71" opacity=".07"/>
<path d="M180,182 L138,244 A75,75 0 0,1 138,120 Z" fill="#e74c3c" opacity=".07"/>
<ellipse cx="180" cy="182" rx="20" ry="60" fill="#0d2040" stroke="#555" stroke-width="1.5"/>
<polygon points="180,117 169,133 191,133" fill="#555"/>
<circle cx="180" cy="137" r="10" fill="#e74c3c"><animate attributeName="opacity" values="1;.4;1" dur="1.5s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="137" r="10" fill="#e74c3c" opacity=".1"><animate attributeName="r" values="13;26;13" dur="1.5s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="162" r="10" fill="#e74c3c"><animate attributeName="opacity" values="1;.4;1" dur="1.5s" begin=".4s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="162" r="10" fill="#e74c3c" opacity=".1"><animate attributeName="r" values="13;26;13" dur="1.5s" begin=".4s" repeatCount="indefinite"/></circle>
<circle cx="200" cy="180" r="6" fill="#2ecc71"><animate attributeName="opacity" values="1;.4;1" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="160" cy="180" r="6" fill="#e74c3c"><animate attributeName="opacity" values="1;.4;1" dur="2s" begin=".5s" repeatCount="indefinite"/></circle>
<circle cx="180" cy="235" r="6" fill="white"><animate attributeName="opacity" values=".9;.4;.9" dur="2s" begin=".9s" repeatCount="indefinite"/></circle>
<text x="196" y="141" fill="#e74c3c" font-size="8.5" font-family="Heebo,sans-serif">אדום 360°</text>
<text x="196" y="166" fill="#e74c3c" font-size="8.5" font-family="Heebo,sans-serif">אדום 360°</text>
<text x="207" y="184" fill="#2ecc71" font-size="8" font-family="Heebo,sans-serif">ירוק</text>
<text x="120" y="184" fill="#e74c3c" font-size="8" font-family="Heebo,sans-serif">אדום</text>
<text x="186" y="250" fill="#ccc" font-size="8" font-family="Heebo,sans-serif">ירכתיים</text>
<rect x="18" y="262" width="324" height="138" rx="8" fill="#0d1e38" stroke="#e74c3c" stroke-width="1.5"/>
<text x="180" y="282" text-anchor="middle" fill="#e74c3c" font-size="13" font-family="Heebo,sans-serif" font-weight="900">NUC עושה דרכה</text>
<text x="180" y="300" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">שני אדומים עגולים + אורות צד + אור ירכתיים</text>
<text x="180" y="317" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">NUC לא בדרכה: שני אדומים בלבד (ללא צד וירכתיים)</text>
<text x="180" y="334" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">אורות הצד מאשרים שהיא אכן בתנועה</text>
<text x="180" y="355" text-anchor="middle" fill="#f39c12" font-size="10" font-family="Heebo,sans-serif" font-weight="700">2 אדומים + ירוק+אדום+ירכתיים = NUC בתנועה</text>
`,
});

// Q279 [ספנות]: approaching a person overboard — from upwind, slowly, so the
// wind drifts the boat down onto the person rather than away from them.
SCENES_QA['mob_approach'] = `
  <rect width="360" height="420" fill="#050d1a"/>
  <circle cx="40" cy="30" r="1.3" fill="white" opacity=".7"/><circle cx="310" cy="50" r="1" fill="white" opacity=".6"/><circle cx="330" cy="20" r="1.2" fill="white" opacity=".8"/>
  <text x="180" y="34" text-anchor="middle" fill="#7eb8f7" font-size="11" font-family="Heebo,sans-serif" font-weight="700">כיוון הרוח</text>
  ${[120,180,240].map((x,i)=>`
    <line x1="${x}" y1="44" x2="${x}" y2="84" stroke="#7eb8f7" stroke-width="2" opacity=".75"/>
    <polygon points="${x},90 ${x-6},78 ${x+6},78" fill="#7eb8f7" opacity=".75"/>
  `).join('')}
  <g transform="rotate(180 180 165)">${topBoat(180,165,'#f1c40f','#c8a000','')}</g>
  <text x="248" y="160" fill="#f1c40f" font-size="10" font-family="Heebo,sans-serif" font-weight="700">מתוך הרוח</text>
  <text x="248" y="174" fill="#f1c40f" font-size="10" font-family="Heebo,sans-serif" font-weight="700">(Upwind), לאט</text>
  <path d="M180,205 Q176,245 180,275" fill="none" stroke="#7eb8f7" stroke-width="2" stroke-dasharray="6,5"/>
  <polygon points="180,283 174,270 186,270" fill="#7eb8f7"/>
  <circle cx="180" cy="300" r="36" fill="none" stroke="#2ecc71" stroke-width="1" opacity=".5"><animate attributeName="r" values="20;40;20" dur="2.4s" repeatCount="indefinite"/><animate attributeName="opacity" values=".6;0;.6" dur="2.4s" repeatCount="indefinite"/></circle>
  <circle cx="180" cy="300" r="9" fill="#e74c3c"/>
  <line x1="174" y1="294" x2="167" y2="285" stroke="#e74c3c" stroke-width="3" stroke-linecap="round"/>
  <line x1="186" y1="294" x2="193" y2="285" stroke="#e74c3c" stroke-width="3" stroke-linecap="round"/>
  <text x="180" y="328" text-anchor="middle" fill="#e74c3c" font-size="11" font-family="Heebo,sans-serif" font-weight="700">אדם בים</text>
  <rect x="18" y="346" width="324" height="58" rx="8" fill="#0d1e38" stroke="#2ecc71" stroke-width="1.5"/>
  <text x="180" y="365" text-anchor="middle" fill="#2ecc71" font-size="12" font-family="Heebo,sans-serif" font-weight="900">MOB — גישה נכונה: מתוך הרוח, באיטיות</text>
  <text x="180" y="384" text-anchor="middle" fill="#aac4e8" font-size="10" font-family="Heebo,sans-serif">הרוח תסחוף את הספינה לעבר האדם, לא ממנו</text>
`;

// ── Compass Rose (שושנה) for license-11 questions ────────────────────────────
// Radii shrunk so the outermost labels + pulsing highlight stay inside the
// scene's vertical safe band (the SVG is drawn with preserveAspectRatio slice,
// which crops ~65 viewBox units off the top and bottom). Before shrinking, the
// north/south vessels' yellow highlight circles fell outside the frame.
const CR_CX = 180, CR_CY = 210, CR_R_TIP = 37, CR_R_BASE = 76, CR_R_LABEL = 88;
const CR_LETTERS = 'ABCDEFGHIJKLMNOP'.split('');
function crPos(angleDeg, radius) {
  const rad = (angleDeg - 90) * Math.PI / 180;
  return { x: CR_CX + radius * Math.cos(rad), y: CR_CY + radius * Math.sin(rad) };
}
function crColor(idx) {
  return ['#1a3fd6','#8a8a8a','#2ecc40','#ff8c1a','#e6007a','#ff8c1a','#2ecc40','#8a8a8a','#e6007a','#8a8a8a','#2ecc40','#ff8c1a','#1a3fd6','#ff8c1a','#2ecc40','#8a8a8a'][idx];
}
function crVessel(letter) {
  const idx = CR_LETTERS.indexOf(letter), angle = idx * 22.5, color = crColor(idx);
  const flip = letter === 'E' || letter === 'I';
  const tip = crPos(angle, flip ? CR_R_BASE : CR_R_TIP);
  const bL = crPos(angle - 5, flip ? CR_R_TIP : CR_R_BASE);
  const bR = crPos(angle + 5, flip ? CR_R_TIP : CR_R_BASE);
  const lbl = crPos(angle, CR_R_LABEL);
  return `<polygon points="${tip.x.toFixed(1)},${tip.y.toFixed(1)} ${bL.x.toFixed(1)},${bL.y.toFixed(1)} ${bR.x.toFixed(1)},${bR.y.toFixed(1)}" fill="${color}" stroke="#000" stroke-width="1.2"/>`
    + `<rect x="${(lbl.x-11).toFixed(1)}" y="${(lbl.y-11).toFixed(1)}" width="22" height="22" fill="#fff" stroke="${color}" stroke-width="2.2"/>`
    + `<text x="${lbl.x.toFixed(1)}" y="${(lbl.y+5).toFixed(1)}" text-anchor="middle" font-family="Arial,sans-serif" font-size="14" font-weight="900" fill="${color}">${letter}</text>`;
}
function crHighlight(letter) {
  const p = crPos(CR_LETTERS.indexOf(letter) * 22.5, CR_R_LABEL);
  return `<circle cx="${p.x.toFixed(1)}" cy="${p.y.toFixed(1)}" r="17" fill="none" stroke="#ffd700" stroke-width="3"><animate attributeName="r" values="13;18;13" dur="1.4s" repeatCount="indefinite"/></circle>`;
}
function crBowLine(letter, color) {
  const idx = CR_LETTERS.indexOf(letter), angle = idx * 22.5, flip = letter === 'E' || letter === 'I';
  const tipR = flip ? CR_R_BASE : CR_R_TIP;
  const from = crPos(angle, tipR), to = crPos(angle, flip ? tipR + 50 : tipR - 45);
  return `<line x1="${from.x.toFixed(1)}" y1="${from.y.toFixed(1)}" x2="${to.x.toFixed(1)}" y2="${to.y.toFixed(1)}" stroke="#111" stroke-width="3.5" stroke-dasharray="6,3" opacity="0.9"/>`;
}
function crBall(cx, cy, r) { return `<circle cx="${cx}" cy="${cy}" r="${r||8}" fill="#111"/>`; }
function crDiamond(cx, cy, s) { s=s||9; const h=s*1.4,w=s*0.65; return `<polygon points="${cx},${cy-h} ${cx+w},${cy} ${cx},${cy+h} ${cx-w},${cy}" fill="#111"/>`; }
function crConeDown(cx, cy, s) { s=s||9; return `<polygon points="${cx-s},${cy-s} ${cx+s},${cy-s} ${cx},${cy+s}" fill="#111"/>`; }
function crConeUp(cx, cy, s) { s=s||9; return `<polygon points="${cx},${cy-s} ${cx+s},${cy+s} ${cx-s},${cy+s}" fill="#111"/>`; }
// Draws a signal flag on a mast using the canonical SIGNAL_FLAGS definitions,
// so the collision-rules diagrams and the flag scenes can never diverge.
function crFlag(cx, cy, letter) {
  const f = SIGNAL_FLAGS[letter];
  if (!f) return '';
  return `<g transform="translate(${cx},${cy})"><line x1="0" y1="-20" x2="0" y2="10" stroke="#333" stroke-width="2"/>`
    + f.draw(1, -20, 18, 14)
    + `<rect x="1" y="-20" width="18" height="14" fill="none" stroke="#111" stroke-width="1"/>`
    + `<text x="10" y="-3" text-anchor="middle" font-family="Arial" font-size="9" font-weight="900" fill="${f.color}">${letter}</text></g>`;
}
const CR_SHAPES = {
  80: (cx,cy) => `<g transform="translate(${cx},${cy})">${crBall(0,-12,6)}${crBall(0,12,6)}<line x1="0" y1="-20" x2="0" y2="20" stroke="#111" stroke-width="2"/></g>`,
  10: (cx,cy) => `<g transform="translate(${cx},${cy})">${crBall(0,-16,6)}${crBall(0,0,6)}${crBall(0,16,6)}<line x1="0" y1="-24" x2="0" y2="24" stroke="#111" stroke-width="2"/></g>`,
  77: (cx,cy) => crBall(cx,cy,10),
  20: (cx,cy) => crConeDown(cx,cy,10),
  75: (cx,cy) => `<rect x="${cx-9}" y="${cy-14}" width="18" height="28" rx="3" fill="#111"/>`,
  76: (cx,cy) => `<g transform="translate(${cx},${cy})">${crBall(0,-14,6)}${crBall(-14,10,6)}${crBall(14,10,6)}<line x1="0" y1="-20" x2="0" y2="4" stroke="#111" stroke-width="2"/><line x1="-14" y1="4" x2="14" y2="4" stroke="#111" stroke-width="2"/></g>`,
  79: (cx,cy) => `<g transform="translate(${cx},${cy})">${crBall(0,-16,6)}${crDiamond(0,0,7)}${crBall(0,16,6)}<line x1="0" y1="-24" x2="0" y2="24" stroke="#111" stroke-width="1.5"/></g>`,
  81: (cx,cy) => `<g transform="translate(${cx},${cy})">${crBall(0,-16,6)}${crBall(0,0,6)}${crBall(0,16,6)}<line x1="0" y1="-24" x2="0" y2="24" stroke="#111" stroke-width="2"/></g>`,
  83: (cx,cy) => `<g transform="translate(${cx},${cy})"><rect x="-8" y="-18" width="16" height="14" fill="#e74c3c" stroke="#111" stroke-width="1.2"/>${crBall(0,10,6)}<line x1="0" y1="-18" x2="0" y2="18" stroke="#111" stroke-width="1.5"/></g>`,
  84: (cx,cy) => `<g transform="translate(${cx},${cy})">${crConeDown(0,-8,9)}${crConeUp(0,10,9)}<line x1="0" y1="-18" x2="0" y2="20" stroke="#111" stroke-width="1.5"/></g>`,
  86: (cx,cy) => crDiamond(cx,cy,12),
  87: (cx,cy) => `<g transform="translate(${cx},${cy})">${crBall(0,-16,6)}${crDiamond(0,0,7)}${crBall(0,16,6)}<line x1="0" y1="-24" x2="0" y2="24" stroke="#111" stroke-width="1.5"/>${crDiamond(18,-8,5)}${crDiamond(18,8,5)}</g>`,
  89: (cx,cy) => `<g transform="translate(${cx},${cy})">${crBall(0,-16,6)}${crDiamond(0,0,7)}${crBall(0,16,6)}<line x1="0" y1="-24" x2="0" y2="24" stroke="#111" stroke-width="1.5"/>${crBall(18,-8,5)}${crBall(18,8,5)}</g>`,
  90: (cx,cy) => `<g transform="translate(${cx},${cy})">${crBall(0,-16,6)}${crDiamond(0,0,7)}${crBall(0,16,6)}<line x1="0" y1="-24" x2="0" y2="24" stroke="#111" stroke-width="1.5"/>${crDiamond(-18,-8,5)}${crDiamond(-18,8,5)}${crBall(18,-8,5)}${crBall(18,8,5)}</g>`,
  // #1057 hoists 93 over 92 and means distress; the distress hoist is N over C.
  92: (cx,cy) => crFlag(cx,cy,'C'),
  93: (cx,cy) => crFlag(cx,cy,'N'),
  95: (cx,cy) => crFlag(cx,cy,'B'),
  98: (cx,cy) => crFlag(cx,cy,'A'),
  104: (cx,cy) => crFlag(cx,cy,'O'),
  106: (cx,cy) => crFlag(cx,cy,'Q'),
};
// shapeIds are listed top-down. withBall appends the black ball that some
// questions describe in prose rather than by image number; it is often the only
// thing distinguishing two otherwise identical questions (#1011 vs #1038).
function crDayShape(letter, shapeIds, withBall) {
  const ids = (Array.isArray(shapeIds) ? shapeIds : [shapeIds]).filter(id => CR_SHAPES[id]);
  if (!ids.length && !withBall) return '';
  const angle = CR_LETTERS.indexOf(letter) * 22.5;
  const shapeR = CR_R_TIP - 17;
  const p = crPos(angle, shapeR);
  const rows = ids.length + (withBall ? 1 : 0);
  const rowH = 36;
  const top = -(rows - 1) * rowH / 2;
  const ry = 32 + (rows - 1) * rowH / 2;
  let svg = `<ellipse cx="${p.x.toFixed(1)}" cy="${p.y.toFixed(1)}" rx="34" ry="${ry.toFixed(1)}" fill="#fff" stroke="#333" stroke-width="1.5" opacity="0.92"/>`;
  ids.forEach((id, i) => { svg += CR_SHAPES[id](p.x, p.y + top + i * rowH); });
  if (withBall) svg += crBall(p.x, p.y + top + ids.length * rowH, 9);
  const lp = crPos(angle, shapeR - 36 - (rows - 1) * rowH / 2);
  const label = `${letter} | תמונה ${ids.join('+')}${withBall ? '+כדור' : ''}`;
  const lw = Math.max(60, label.length * 5.2);
  svg += `<rect x="${(lp.x-lw/2).toFixed(1)}" y="${(lp.y-7).toFixed(1)}" width="${lw.toFixed(1)}" height="14" rx="3" fill="#0c1a3a" opacity="0.85"/>`;
  svg += `<text x="${lp.x.toFixed(1)}" y="${(lp.y+4).toFixed(1)}" text-anchor="middle" font-family="Heebo,sans-serif" font-size="8.5" font-weight="700" fill="#fff">${label}</text>`;
  return svg;
}
const SIGNAL_IMAGES = {
  111: ['S'],
  112: ['S','S'],
  113: ['S','S','S'],
  114: ['S','S','S'],
  115: ['L','S','S'],
  116: ['L','S','L','S'],
  117: ['L','L'],
  118: ['L'],
  119: ['S','S','S','S','S'],
  120: ['L','S'],
  121: ['L','S','S','S'],
  122: ['L','L','S'],
  123: ['L','S','S'],
  124: ['L','S','L','S'],
  125: ['L','L','L','L','L','L','L'],
  126: ['S','S','S','S','S','S','S','S','S','S','S','S'],
};

function generateCompassRoseScene(qText) {
  const txt = qText || '';
  const parenMatch = txt.match(/\(([A-P])\)/g);
  const quoteMatch = txt.match(/[""״"]([A-P])[""״"]/g);
  const bareMatch = txt.match(/(?:כלי.(?:ה)?שייט|אופנוע.{0,3}ים|מפרשית)\s+([A-P])\b/g);
  let vessels;
  if (parenMatch && parenMatch.length >= 2) {
    vessels = parenMatch.map(v => v.replace(/[()]/g, ''));
  } else if (quoteMatch && quoteMatch.length >= 2) {
    vessels = quoteMatch.map(v => v.replace(/[""״"]/g, ''));
  } else if (bareMatch) {
    vessels = bareMatch.map(m => m.match(/([A-P])$/)[1]);
  } else {
    vessels = [];
  }
  // Every image in the question, in text order. "X ומעליו Y" states Y sits above
  // X, so that phrasing flips the text order into display (top-down) order.
  let shapeIds = (txt.match(/תמונה\s*[""״"(]?(\d+)/g) || [])
    .map(m => parseInt(m.match(/(\d+)/)[1], 10));
  if (shapeIds.length > 1 && /ומעליו/.test(txt)) shapeIds.reverse();
  const withBall = /כדור שחור/.test(txt);
  const observer = vessels[0] || null, target = vessels[1] || null;
  if (!observer || !target) return null;
  const D = CR_R_LABEL + 20;
  const d45 = Math.round(D * 0.707);
  let svg = `<rect x="10" y="10" width="340" height="400" fill="#fff" stroke="#0c1a3a" stroke-width="2"/>`;
  svg += `<line x1="${CR_CX}" y1="${CR_CY-D}" x2="${CR_CX}" y2="${CR_CY+D}" stroke="#333" stroke-width="0.6" stroke-dasharray="2,2"/>`;
  svg += `<line x1="${CR_CX-D}" y1="${CR_CY}" x2="${CR_CX+D}" y2="${CR_CY}" stroke="#333" stroke-width="0.6" stroke-dasharray="2,2"/>`;
  svg += `<line x1="${CR_CX-d45}" y1="${CR_CY-d45}" x2="${CR_CX+d45}" y2="${CR_CY+d45}" stroke="#333" stroke-width="0.5" stroke-dasharray="2,2"/>`;
  svg += `<line x1="${CR_CX+d45}" y1="${CR_CY-d45}" x2="${CR_CX-d45}" y2="${CR_CY+d45}" stroke="#333" stroke-width="0.5" stroke-dasharray="2,2"/>`;
  for (const l of CR_LETTERS) svg += crVessel(l);
  if ((shapeIds.length || withBall) && target) svg += crDayShape(target, shapeIds, withBall);
  if (observer) svg += crBowLine(observer, '#ffd700');
  if (target) svg += crBowLine(target, '#e74c3c');
  if (observer) svg += crHighlight(observer);
  if (target) svg += crHighlight(target);
  const shapeId = shapeIds[0] || null;
  const hasShape = shapeIds.some(id => CR_SHAPES[id]) || withBall;
  const signalPattern = shapeId && SIGNAL_IMAGES[shapeId];
  // The in-SVG caption was dropped: it duplicated the footer question and lived
  // in the cropped top band anyway. The signal pattern moves up into the safe
  // band (was SY=385, below the crop line and invisible).
  if (signalPattern) {
    // Compact box wrapping its own content, anchored top-left where the rose
    // leaves a corner free, so it never collides with the north vessel.
    const SR=6, LW=30, LH=12, GAP=6, PAD=8;
    const contentW = signalPattern.reduce((s,b) => s + (b==='L' ? LW : SR*2), 0) + GAP*(signalPattern.length-1);
    const boxW = Math.max(contentW + PAD*2, 62);
    const BX=16, BY=104, BH=34, LY=BY+12, SY=BY+25;
    let sx = BX + (boxW - contentW)/2;
    svg += `<rect x="${BX}" y="${BY}" width="${boxW.toFixed(0)}" height="${BH}" rx="6" fill="#0c1a3a" stroke="#e74c3c" stroke-width="1"/>`;
    svg += `<text x="${(BX+boxW/2).toFixed(0)}" y="${LY}" text-anchor="middle" fill="#e74c3c" font-size="8" font-family="Heebo,sans-serif">תמונה ${shapeId}</text>`;
    signalPattern.forEach(b => {
      if (b==='L') {
        svg += `<rect x="${sx.toFixed(1)}" y="${SY-LH/2}" width="${LW}" height="${LH}" rx="3" fill="#e74c3c"/>`;
        sx += LW + GAP;
      } else {
        svg += `<circle cx="${(sx+SR).toFixed(1)}" cy="${SY}" r="${SR}" fill="#e74c3c"/>`;
        sx += SR*2 + GAP;
      }
    });
  }
  return svg;
}

// סכנות רכיבה ותמרון — מי חשוף לסכנה: הנוהג אוחז בהגה, הנוסע מאחור לא
SCENES_QA['pwc_rider_risk'] = `
  <rect width="360" height="420" fill="#0a1428"/>
  <rect x="0" y="286" width="360" height="134" fill="#1a5276"/>
  <g opacity="0.12">
    <path d="M0 330 Q90 322 180 330 Q270 338 360 330" fill="none" stroke="white" stroke-width="1.5"/>
    <path d="M0 372 Q90 364 180 372 Q270 380 360 372" fill="none" stroke="white" stroke-width="1.5"/>
  </g>
  <text x="180" y="134" text-anchor="middle" fill="#fff" font-size="17" font-family="Heebo,sans-serif" font-weight="900">מי חשוף לסכנה?</text>

  <!-- jet stream off the nozzle: where the thrown passenger ends up -->
  <g opacity=".5">
    <path d="M120 322 Q92 326 64 334" fill="none" stroke="#aed6f1" stroke-width="6" stroke-linecap="round"/>
    <path d="M120 328 Q96 336 72 346" fill="none" stroke="#aed6f1" stroke-width="4" stroke-linecap="round"/>
    <path d="M120 317 Q94 318 68 322" fill="none" stroke="#aed6f1" stroke-width="2.5" stroke-linecap="round"/>
  </g>
  <text x="74" y="306" text-anchor="middle" fill="#aed6f1" font-size="11" font-family="Heebo,sans-serif" font-weight="700">סילון המים</text>

  ${sideJetSki(200, 318, '#f1c40f', '#c8a000', 1.3)}

  <!-- braced: hands on the bars, feet in the footwell -->
  ${sideRider(197, 292, 1.25, 'grip', '#2980b9')}

  <!-- flung off the saddle, still in the air, heading for the jet stream -->
  <path d="M170 288 Q152 268 138 254" fill="none" stroke="#e74c3c" stroke-width="2"
        stroke-dasharray="5 4" opacity=".75"/>
  <path d="M136 252 L144 260 L134 262 Z" fill="#e74c3c" opacity=".75"/>
  ${sideRider(128, 258, 1.1, 'thrown', '#e74c3c')}

  <!-- callouts, centred so RTL cannot smear them across the artwork, and kept
       clear of the figures they point at -->
  <text x="292" y="216" text-anchor="middle" fill="#2ecc71" font-size="13" font-family="Heebo,sans-serif" font-weight="900">הנוהג</text>
  <text x="292" y="232" text-anchor="middle" fill="#2ecc71" font-size="11" font-family="Heebo,sans-serif">אוחז בהגה</text>
  <text x="292" y="247" text-anchor="middle" fill="#2ecc71" font-size="11" font-family="Heebo,sans-serif">אחיזה טובה יותר</text>
  <path d="M278 252 Q252 260 228 266" fill="none" stroke="#2ecc71" stroke-width="1.6" opacity=".7"/>

  <text x="88" y="160" text-anchor="middle" fill="#e74c3c" font-size="13" font-family="Heebo,sans-serif" font-weight="900">הנוסע מאחור</text>
  <text x="88" y="176" text-anchor="middle" fill="#e74c3c" font-size="11" font-family="Heebo,sans-serif">אין לו במה לאחוז</text>
  <text x="88" y="191" text-anchor="middle" fill="#e74c3c" font-size="11" font-family="Heebo,sans-serif">נזרק לים אל הסילון</text>
  <path d="M96 198 Q106 208 112 218" fill="none" stroke="#e74c3c" stroke-width="1.6" opacity=".7"/>
`;

// סכנות רכיבה ותמרון — מעבר גלי חוף במהירות: עף מעל הגל ונוחת בלי שליטה
SCENES_QA['pwc_wave_launch'] = `
  <rect width="360" height="420" fill="#0a1428"/>
  <text x="180" y="134" text-anchor="middle" fill="#fff" font-size="16" font-family="Heebo,sans-serif" font-weight="900">גלי חוף במהירות גבוהה מדי</text>

  <!-- the sea, with one steep shore wave the craft has just cleared -->
  <path d="M0 420 L0 322 Q52 320 96 300 Q126 286 150 250 Q168 276 200 296
           Q246 320 300 318 Q334 317 360 320 L360 420 Z" fill="#1a5276"/>
  <path d="M150 250 Q160 266 176 280 Q160 274 150 276 Q142 262 150 250 Z" fill="#eaf4fb" opacity=".85"/>
  <g opacity="0.12">
    <path d="M206 348 Q268 342 360 346" fill="none" stroke="white" stroke-width="1.5"/>
    <path d="M0 372 Q90 366 180 372 Q270 378 360 372" fill="none" stroke="white" stroke-width="1.5"/>
  </g>

  <!-- flight path off the crest down to the slam -->
  <path d="M158 244 Q212 200 268 262" fill="none" stroke="#e74c3c" stroke-width="2"
        stroke-dasharray="6 5" opacity=".8"/>

  <!-- airborne, bow already dropping -->
  <g transform="translate(258,250) rotate(30)">
    ${sideJetSki(0, 0, '#f1c40f', '#c8a000', 0.8)}
    ${sideRider(-2, -16, 0.78, 'grip', '#2980b9')}
  </g>

  <!-- impact burst where it comes down -->
  <g opacity=".8">
    <path d="M282 292 L288 276" stroke="#eaf4fb" stroke-width="2.5" stroke-linecap="round"/>
    <path d="M296 296 L306 284" stroke="#eaf4fb" stroke-width="2.5" stroke-linecap="round"/>
    <path d="M270 296 L264 282" stroke="#eaf4fb" stroke-width="2.5" stroke-linecap="round"/>
  </g>

  <text x="96" y="182" text-anchor="middle" fill="#7eb8f7" font-size="12" font-family="Heebo,sans-serif" font-weight="700">עובר את הגל</text>
  <text x="96" y="198" text-anchor="middle" fill="#7eb8f7" font-size="12" font-family="Heebo,sans-serif" font-weight="700">מהר מדי</text>

  <text x="272" y="176" text-anchor="middle" fill="#e74c3c" font-size="13" font-family="Heebo,sans-serif" font-weight="900">נופל אחרי הגל</text>
  <text x="272" y="192" text-anchor="middle" fill="#e74c3c" font-size="11" font-family="Heebo,sans-serif">ומאבד שליטה</text>

  <text x="180" y="320" text-anchor="middle" fill="#fff" font-size="12" font-family="Heebo,sans-serif" font-weight="700">האט לפני גלי החוף</text>
`;

// סכנות רכיבה ותמרון — גלים גבוהים מהצד: סכנת התהפכות
SCENES_QA['pwc_beam_capsize'] = `
  <rect width="360" height="420" fill="#0a1428"/>
  <text x="180" y="134" text-anchor="middle" fill="#fff" font-size="16" font-family="Heebo,sans-serif" font-weight="900">גלים גבוהים מהצד</text>

  <!-- water, with the beam wave stacked up on the right -->
  <path d="M0 420 L0 300 Q80 296 150 302 Q220 308 268 268 Q292 246 312 232
           Q336 250 360 268 L360 420 Z" fill="#1a5276"/>
  <path d="M312 232 Q330 246 344 262 Q324 252 308 254 Q306 242 312 232 Z" fill="#eaf4fb" opacity=".85"/>
  <g opacity="0.12"><path d="M0 350 Q90 344 180 350 Q270 356 360 352" fill="none" stroke="white" stroke-width="1.5"/></g>

  <!-- the craft end-on, already heeled away from the wave -->
  <g transform="translate(168,296) rotate(-32)">
    ${sternJetSki(0, 0, 1.05, '#2980b9')}
  </g>

  <!-- the wave shoving the hull from the side -->
  <path d="M268 272 L222 288" stroke="#e74c3c" stroke-width="3" stroke-linecap="round"/>
  <path d="M222 288 L233 284 L232 294 Z" fill="#e74c3c"/>

  <!-- roll arrow over the top -->
  <path d="M212 198 A50 50 0 0 0 128 220" fill="none" stroke="#e74c3c" stroke-width="2.5" stroke-dasharray="6 5"/>
  <path d="M128 220 L139 217 L134 227 Z" fill="#e74c3c"/>

  <text x="180" y="176" text-anchor="middle" fill="#e74c3c" font-size="14" font-family="Heebo,sans-serif" font-weight="900">סכנת התהפכות</text>

  <text x="284" y="292" text-anchor="middle" fill="#7eb8f7" font-size="11" font-family="Heebo,sans-serif" font-weight="700">הגל בא מהצד</text>
  <text x="180" y="320" text-anchor="middle" fill="#fff" font-size="12" font-family="Heebo,sans-serif" font-weight="700">האט וקבל את הגלים באלכסון</text>
`;

// סכנות רכיבה ותמרון — גישה לכלי שיט אחר: לאט, נגד הרוח, בלי גלים
SCENES_QA['pwc_slow_approach'] = `
  <rect width="360" height="420" fill="#0a1428"/>
  <rect x="0" y="244" width="360" height="176" fill="#1a5276"/>
  <text x="180" y="134" text-anchor="middle" fill="#fff" font-size="16" font-family="Heebo,sans-serif" font-weight="900">גישה לכלי שיט אחר</text>

  <!-- barely a ripple between them: the whole point of going slow -->
  <g opacity="0.16">
    <path d="M0 306 Q90 302 180 306 Q270 310 360 306" fill="none" stroke="white" stroke-width="1.5"/>
    <path d="M0 352 Q90 348 180 352 Q270 356 360 352" fill="none" stroke="white" stroke-width="1.5"/>
  </g>

  <!-- the vessel being approached, lying stopped -->
  <g transform="translate(262,272) scale(0.52)">
    ${sideBoat(0, 0, '#ecf0f1', '#95a5a6')}
  </g>

  <!-- our craft, coming up slowly from astern of it -->
  ${sideJetSki(108, 282, '#f1c40f', '#c8a000', 0.82)}
  ${sideRider(106, 266, 0.8, 'grip', '#2980b9')}

  <!-- wind on the nose: approach against it so the craft slows itself -->
  <path d="M316 190 L240 190" stroke="#7eb8f7" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M240 190 L250 185 L250 195 Z" fill="#7eb8f7"/>
  <text x="278" y="180" text-anchor="middle" fill="#7eb8f7" font-size="11" font-family="Heebo,sans-serif" font-weight="700">הרוח</text>
  <text x="272" y="212" text-anchor="middle" fill="#7eb8f7" font-size="11" font-family="Heebo,sans-serif">התקרב נגד הרוח</text>

  <!-- slow-speed callout on our craft -->
  <text x="82" y="180" text-anchor="middle" fill="#2ecc71" font-size="13" font-family="Heebo,sans-serif" font-weight="900">מהירות מינימלית</text>
  <text x="82" y="196" text-anchor="middle" fill="#2ecc71" font-size="11" font-family="Heebo,sans-serif">כדי לא לייצר גלים</text>
  <path d="M90 204 Q96 218 100 230" fill="none" stroke="#2ecc71" stroke-width="1.6" opacity=".7"/>

  <text x="180" y="320" text-anchor="middle" fill="#fff" font-size="12" font-family="Heebo,sans-serif" font-weight="700">דומם מנוע בקרבת כלי השיט</text>
`;

// תמרוני ספינה — גרירת סקי או בננה: מורשה ל-3, שניים על הכלי, קשר עין
SCENES_QA['tow_skier'] = `
  <rect width="360" height="420" fill="#0a1428"/>
  <rect x="0" y="150" width="360" height="270" fill="#1a5276"/>
  <g opacity="0.1">
    <path d="M0 250 Q90 244 180 250 Q270 256 360 250" fill="none" stroke="white" stroke-width="1.5"/>
    <path d="M0 340 Q90 334 180 340 Q270 346 360 340" fill="none" stroke="white" stroke-width="1.5"/>
  </g>
  <text x="180" y="134" text-anchor="middle" fill="#fff" font-size="16" font-family="Heebo,sans-serif" font-weight="900">גרירת סקי או בננה</text>

  <!-- the towing craft, seen from above, running to the right -->
  ${topJetSki(238, 214, 1, '#f1c40f', '#c8a000', 0)}
  <circle cx="228" cy="208" r="5" fill="#2980b9"/>
  <circle cx="212" cy="212" r="5" fill="#e67e22"/>
  <text x="238" y="182" text-anchor="middle" fill="#2ecc71" font-size="12" font-family="Heebo,sans-serif" font-weight="900">2 אנשים על הכלי</text>

  <!-- tow rope back to the skier -->
  <path d="M186 216 L104 240" stroke="#ecf0f1" stroke-width="2" opacity=".85"/>

  <!-- the towed rider -->
  <g transform="translate(94,244)">
    <ellipse rx="15" ry="7" fill="#e74c3c" opacity=".9"/>
    <circle cy="-11" r="6" fill="#f5cba7"/>
  </g>
  <text x="88" y="272" text-anchor="middle" fill="#e74c3c" font-size="11" font-family="Heebo,sans-serif" font-weight="700">הנגרר</text>

  <!-- eye contact from the rear rider back to the towed rider -->
  <path d="M206 216 Q158 220 110 234" fill="none" stroke="#2ecc71" stroke-width="1.6" stroke-dasharray="5 4" opacity=".85"/>
  <text x="164" y="204" text-anchor="middle" fill="#2ecc71" font-size="11" font-family="Heebo,sans-serif" font-weight="700">קשר עין רצוף</text>

  <text x="180" y="308" text-anchor="middle" fill="#fff" font-size="13" font-family="Heebo,sans-serif" font-weight="900">האופנוע חייב להיות מורשה ל-3 רוכבים</text>
  <text x="180" y="326" text-anchor="middle" fill="#7eb8f7" font-size="11.5" font-family="Heebo,sans-serif">נהג + צופה לאחור = לפחות 2 על הכלי</text>
`;

// תמרוני ספינה — גרירת אופנוע ים אחר: נקודות הקשירה ואורך החבל
SCENES_QA['tow_craft'] = `
  <rect width="360" height="420" fill="#0a1428"/>
  <rect x="0" y="150" width="360" height="270" fill="#1a5276"/>
  <g opacity="0.1"><path d="M0 320 Q90 314 180 320 Q270 326 360 320" fill="none" stroke="white" stroke-width="1.5"/></g>
  <text x="180" y="134" text-anchor="middle" fill="#fff" font-size="16" font-family="Heebo,sans-serif" font-weight="900">גרירת אופנוע ים</text>

  <!-- the tug, ahead and to the right -->
  ${topJetSki(268, 200, 0.82, '#f1c40f', '#c8a000', 0)}
  <text x="268" y="172" text-anchor="middle" fill="#f1c40f" font-size="11" font-family="Heebo,sans-serif" font-weight="700">הגורר</text>
  <circle cx="248" cy="206" r="4.5" fill="#e74c3c"/>

  <!-- the rope between them, label kept off the line -->
  <path d="M230 206 L128 262" stroke="#ecf0f1" stroke-width="2" opacity=".85"/>
  <text x="170" y="178" text-anchor="middle" fill="#2ecc71" font-size="15" font-family="Heebo,sans-serif" font-weight="900">40 מטר</text>
  <text x="170" y="194" text-anchor="middle" fill="#2ecc71" font-size="11" font-family="Heebo,sans-serif">אורך החבל המומלץ</text>

  <!-- the towed craft, astern and to the left -->
  ${topJetSki(96, 270, 0.82, '#95a5a6', '#6b7778', 0)}
  <text x="96" y="300" text-anchor="middle" fill="#95a5a6" font-size="11" font-family="Heebo,sans-serif" font-weight="700">הנגרר</text>
  <circle cx="130" cy="266" r="4.5" fill="#e74c3c"/>

  <!-- the two attachment points, called out on separate lines low and clear -->
  <text x="180" y="330" text-anchor="middle" fill="#e74c3c" font-size="11.5" font-family="Heebo,sans-serif" font-weight="700">בנגרר: בתפס הקדמי</text>
  <text x="180" y="314" text-anchor="middle" fill="#e74c3c" font-size="11.5" font-family="Heebo,sans-serif" font-weight="700">אצלי: מסביב למושב או בתפס אחורי</text>
`;

// תמרוני ספינה — יישור אופנוע שהתהפך: לכיוון שהיצרן קבע
SCENES_QA['right_capsized'] = `
  <rect width="360" height="420" fill="#0a1428"/>
  <rect x="0" y="176" width="360" height="244" fill="#1a5276"/>
  <text x="180" y="134" text-anchor="middle" fill="#fff" font-size="16" font-family="Heebo,sans-serif" font-weight="900">אופנוע ים שהתהפך</text>

  <!-- Upside down: hull only. The rider is in the water in both questions here,
       and rotating the full sternJetSki put a head under the boat that read as
       a blob rather than as a capsize. -->
  <g transform="translate(102,244)">
    <path d="M-26,6 L26,6 Q23,-10 0,-14 Q-23,-10 -26,6 Z"
          fill="#c8a000" stroke="#8a7000" stroke-width="1.4" stroke-linejoin="round"/>
    <path d="M-27,6 L27,6 L24,14 L-24,14 Z" fill="#f1c40f" stroke="#c8a000" stroke-width="1.4" stroke-linejoin="round"/>
  </g>
  <text x="102" y="278" text-anchor="middle" fill="#e74c3c" font-size="11.5" font-family="Heebo,sans-serif" font-weight="700">הפוך</text>

  <!-- the righting arc -->
  <path d="M136 214 A54 54 0 0 1 224 214" fill="none" stroke="#2ecc71" stroke-width="2.5" stroke-dasharray="6 5"/>
  <path d="M224 214 L214 210 L218 220 Z" fill="#2ecc71"/>
  <text x="180" y="196" text-anchor="middle" fill="#2ecc71" font-size="12" font-family="Heebo,sans-serif" font-weight="900">לפי הוראת היצרן</text>

  <!-- upright again -->
  ${sternJetSki(262, 244, 0.8, '#2980b9')}
  <text x="262" y="272" text-anchor="middle" fill="#2ecc71" font-size="11" font-family="Heebo,sans-serif" font-weight="700">ישר</text>

  <rect x="44" y="292" width="272" height="34" rx="8" fill="#0d3d2a" stroke="#2ecc71" stroke-width="2"/>
  <text x="180" y="314" text-anchor="middle" fill="#2ecc71" font-size="12.5" font-family="Heebo,sans-serif" font-weight="900">הכיוון מסומן על גוף האופנוע</text>
`;

// תמרוני ספינה — החפה: למקם את האופנוע בין שני גלים כדי לשמור שליטה
SCENES_QA['beaching'] = `
  <rect width="360" height="420" fill="#0a1428"/>
  <text x="180" y="132" text-anchor="middle" fill="#fff" font-size="16" font-family="Heebo,sans-serif" font-weight="900">החפה בגלי חוף</text>

  <!-- shore on the right, sea to the left, two wave crests with a trough between -->
  <path d="M0 420 L0 206 Q40 188 78 206 Q104 218 128 206 Q168 186 208 206
           Q236 220 262 210 L262 420 Z" fill="#1a5276"/>
  <path d="M262 210 Q290 218 318 234 L360 234 L360 420 L262 420 Z" fill="#d9c08a"/>
  <path d="M78 206 Q92 196 104 210 Q92 204 78 206 Z" fill="#eaf4fb" opacity=".85"/>
  <path d="M208 206 Q222 196 234 210 Q222 204 208 206 Z" fill="#eaf4fb" opacity=".85"/>

  <text x="70" y="186" text-anchor="middle" fill="#7eb8f7" font-size="11.5" font-family="Heebo,sans-serif" font-weight="700">גל</text>
  <text x="216" y="186" text-anchor="middle" fill="#7eb8f7" font-size="11.5" font-family="Heebo,sans-serif" font-weight="700">גל</text>

  <!-- the craft sitting in the trough -->
  ${sideJetSki(148, 224, '#f1c40f', '#c8a000', 0.7)}

  <!-- the gap it sits in -->
  <path d="M108 250 L188 250" stroke="#2ecc71" stroke-width="1.8"/>
  <path d="M108 250 L116 246 L116 254 Z" fill="#2ecc71"/>
  <path d="M188 250 L180 246 L180 254 Z" fill="#2ecc71"/>
  <text x="148" y="270" text-anchor="middle" fill="#2ecc71" font-size="13" font-family="Heebo,sans-serif" font-weight="900">בין שני גלים</text>

  <text x="312" y="268" text-anchor="middle" fill="#8a7350" font-size="11.5" font-family="Heebo,sans-serif" font-weight="700">החוף</text>
  <text x="180" y="312" text-anchor="middle" fill="#fff" font-size="13" font-family="Heebo,sans-serif" font-weight="900">כך נשמרת שליטה על האופנוע</text>
`;

// עזרה ראשונה — מחוסר הכרה: קודם כל נשימה ודופק
SCENES_QA['firstaid_abc'] = `
  <rect width="360" height="420" fill="#0a1428"/>
  <text x="180" y="136" text-anchor="middle" fill="#fff" font-size="17" font-family="Heebo,sans-serif" font-weight="900">נפגע מחוסר הכרה</text>

  <rect x="58" y="158" width="244" height="42" rx="8" fill="#0d3d2a" stroke="#2ecc71" stroke-width="2"/>
  <text x="180" y="177" text-anchor="middle" fill="#2ecc71" font-size="15" font-family="Heebo,sans-serif" font-weight="900">בדוק נשימה ודופק</text>
  <text x="180" y="193" text-anchor="middle" fill="#7fd8a8" font-size="11" font-family="Heebo,sans-serif">לפני כל פעולה אחרת</text>

  <!-- deck he is lying on -->
  <rect x="0" y="296" width="360" height="8" fill="#1a5276" opacity=".55"/>
  ${lyingPerson(190, 296, 1.15)}

  <!-- what to check, pointed at the mouth and the neck -->
  <text x="98" y="236" text-anchor="middle" fill="#7eb8f7" font-size="12" font-family="Heebo,sans-serif" font-weight="700">נשימה</text>
  <path d="M104 244 Q118 254 130 268" fill="none" stroke="#7eb8f7" stroke-width="1.6" opacity=".75"/>
  <text x="242" y="236" text-anchor="middle" fill="#7eb8f7" font-size="12" font-family="Heebo,sans-serif" font-weight="700">דופק</text>
  <path d="M232 244 Q198 256 172 272" fill="none" stroke="#7eb8f7" stroke-width="1.6" opacity=".75"/>

  <text x="180" y="326" text-anchor="middle" fill="#fff" font-size="12" font-family="Heebo,sans-serif" font-weight="700">רק אחר כך הנשמה או עיסוי</text>
`;

// עזרה ראשונה — נפגע טביעה שאינו נושם: מה אין לעשות
// The bank's options still describe the mouth-to-mouth era. The answer stays as
// the bank has it, but the order shown here follows current practice: call for
// help first, and compress rather than ventilate. Alex's call, 2026-07-20.
SCENES_QA['firstaid_drowning'] = `
  <rect width="360" height="420" fill="#0a1428"/>
  <text x="180" y="134" text-anchor="middle" fill="#fff" font-size="16" font-family="Heebo,sans-serif" font-weight="900">נפגע טביעה שאינו נושם</text>

  ${tick(276, 166, 1.25)}
  <text x="164" y="171" text-anchor="middle" fill="#2ecc71" font-size="12.5" font-family="Heebo,sans-serif" font-weight="700">הזעק עזרה רפואית</text>
  ${tick(276, 192, 1.25)}
  <text x="164" y="197" text-anchor="middle" fill="#2ecc71" font-size="12.5" font-family="Heebo,sans-serif" font-weight="700">נקה את הפה משאריות</text>
  ${tick(276, 218, 1.25)}
  <text x="164" y="223" text-anchor="middle" fill="#2ecc71" font-size="12.5" font-family="Heebo,sans-serif" font-weight="700">השכב על הגב</text>
  ${tick(276, 244, 1.25)}
  <text x="164" y="249" text-anchor="middle" fill="#2ecc71" font-size="12.5" font-family="Heebo,sans-serif" font-weight="700">עסה את בית החזה</text>

  <rect x="52" y="266" width="256" height="38" rx="8" fill="#2a1010" stroke="#e74c3c" stroke-width="2"/>
  ${cross(286, 285, 1.3)}
  <text x="164" y="290" text-anchor="middle" fill="#e74c3c" font-size="13" font-family="Heebo,sans-serif" font-weight="900">אל תנסה להוציא מים מהריאות</text>

  <rect x="0" y="326" width="360" height="6" fill="#1a5276" opacity=".55"/>
  ${lyingPerson(186, 326, 0.7)}
`;

// עזרה ראשונה — צריבת מדוזה: חומץ, לא מים מתוקים ולא שפשוף
SCENES_QA['firstaid_jellyfish'] = `
  <rect width="360" height="420" fill="#0a1428"/>
  <rect x="0" y="150" width="360" height="270" fill="#1a5276" opacity=".35"/>
  <text x="180" y="136" text-anchor="middle" fill="#fff" font-size="17" font-family="Heebo,sans-serif" font-weight="900">צריבת מדוזה</text>

  <!-- the jellyfish -->
  <g transform="translate(92,206)">
    <path d="M-30 6 Q-30 -22 0 -22 Q30 -22 30 6 Q16 12 0 12 Q-16 12 -30 6 Z" fill="#d6b3e8" opacity=".92"/>
    <path d="M-30 6 Q-15 0 0 6 Q15 12 30 6" fill="none" stroke="#a97bc4" stroke-width="2"/>
    <path d="M-20 10 Q-24 30 -16 46" fill="none" stroke="#d6b3e8" stroke-width="2.5" stroke-linecap="round"/>
    <path d="M-7 12 Q-10 34 -2 52" fill="none" stroke="#d6b3e8" stroke-width="2.5" stroke-linecap="round"/>
    <path d="M7 12 Q11 34 4 52" fill="none" stroke="#d6b3e8" stroke-width="2.5" stroke-linecap="round"/>
    <path d="M20 10 Q25 30 17 46" fill="none" stroke="#d6b3e8" stroke-width="2.5" stroke-linecap="round"/>
  </g>

  <!-- the stung forearm -->
  <g transform="translate(244,206)">
    <rect x="-38" y="-13" width="76" height="26" rx="13" fill="#f5cba7"/>
    <path d="M-22 -4 L-6 4 M-4 -6 L12 2 M14 -3 L26 4" stroke="#e74c3c" stroke-width="3" stroke-linecap="round"/>
  </g>
  <text x="244" y="240" text-anchor="middle" fill="#e74c3c" font-size="11" font-family="Heebo,sans-serif" font-weight="700">אזור הצריבה</text>

  ${cross(300, 268, 1.2)}
  <text x="214" y="272" text-anchor="middle" fill="#e74c3c" font-size="11.5" font-family="Heebo,sans-serif" font-weight="700">לא לשפשף ולא לגרד</text>

  <!-- vinegar -->
  <g transform="translate(110,300)">
    <rect x="-11" y="-24" width="22" height="34" rx="4" fill="#c9a227" stroke="#8a6f16" stroke-width="1.5"/>
    <rect x="-4" y="-31" width="8" height="8" fill="#8a6f16"/>
    <path d="M11 -14 Q30 -8 44 2" fill="none" stroke="#c9a227" stroke-width="3" stroke-linecap="round" opacity=".8"/>
  </g>
  <text x="180" y="326" text-anchor="middle" fill="#2ecc71" font-size="13.5" font-family="Heebo,sans-serif" font-weight="900">שטוף בחומץ או באמוניה מהולה</text>
`;

// עזרה ראשונה — מכת חום: צל ומים
SCENES_QA['firstaid_heatstroke'] = `
  <rect width="360" height="420" fill="#0a1428"/>
  <text x="180" y="134" text-anchor="middle" fill="#fff" font-size="17" font-family="Heebo,sans-serif" font-weight="900">מכת חום</text>

  <!-- sun beating down on the left -->
  <g transform="translate(78,190)">
    <circle r="20" fill="#f39c12"/>
    <g stroke="#f39c12" stroke-width="3" stroke-linecap="round">
      <path d="M0 -30 L0 -38"/><path d="M0 30 L0 38"/><path d="M-30 0 L-38 0"/><path d="M30 0 L38 0"/>
      <path d="M-21 -21 L-27 -27"/><path d="M21 21 L27 27"/><path d="M-21 21 L-27 27"/><path d="M21 -21 L27 -27"/>
    </g>
  </g>

  <!-- shade the casualty is moved into -->
  <path d="M186 214 Q246 178 306 214 Z" fill="#2ecc71" opacity=".85"/>
  <path d="M246 214 L246 268" stroke="#7f8c8d" stroke-width="3.5"/>
  <text x="246" y="176" text-anchor="middle" fill="#2ecc71" font-size="13" font-family="Heebo,sans-serif" font-weight="900">צל</text>

  <!-- arrow from the sun to the shade -->
  <path d="M116 218 Q152 244 186 246" fill="none" stroke="#2ecc71" stroke-width="2.5" stroke-dasharray="6 5"/>
  <path d="M186 246 L175 242 L177 252 Z" fill="#2ecc71"/>

  <rect x="0" y="290" width="360" height="8" fill="#1a5276" opacity=".55"/>
  ${lyingPerson(252, 290, 0.95)}

  <!-- water -->
  <g transform="translate(150,278)">
    <rect x="-9" y="-22" width="18" height="30" rx="3" fill="#7eb8f7" opacity=".9"/>
    <rect x="-3.5" y="-28" width="7" height="7" fill="#4a90d9"/>
  </g>
  <text x="150" y="306" text-anchor="middle" fill="#7eb8f7" font-size="11" font-family="Heebo,sans-serif" font-weight="700">מים</text>

  <text x="180" y="326" text-anchor="middle" fill="#fff" font-size="12.5" font-family="Heebo,sans-serif" font-weight="700">העבר לצל והשקה בהדרגה</text>
`;

// עזרה ראשונה — חשד לשבר: לא לפשוט בגדים ולא להזיז
SCENES_QA['firstaid_fracture'] = `
  <rect width="360" height="420" fill="#0a1428"/>
  <text x="180" y="136" text-anchor="middle" fill="#fff" font-size="17" font-family="Heebo,sans-serif" font-weight="900">חשד לשבר בגף</text>

  <!-- the limb, with the break marked and a splint alongside -->
  <g transform="translate(180,236)">
    <rect x="-76" y="-15" width="152" height="30" rx="15" fill="#f5cba7"/>
    <path d="M-4 -17 L4 -6 L-5 2 L4 15" fill="none" stroke="#e74c3c" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
    <rect x="-70" y="20" width="140" height="9" rx="4" fill="#c9a227"/>
    <rect x="-46" y="-22" width="12" height="56" rx="3" fill="#ecf0f1" opacity=".85"/>
    <rect x="34" y="-22" width="12" height="56" rx="3" fill="#ecf0f1" opacity=".85"/>
  </g>
  <text x="180" y="288" text-anchor="middle" fill="#2ecc71" font-size="12.5" font-family="Heebo,sans-serif" font-weight="900">תמוך באבר במצב שבו הוא נמצא</text>

  <rect x="46" y="164" width="268" height="34" rx="8" fill="#2a1010" stroke="#e74c3c" stroke-width="2"/>
  ${cross(292, 181, 1.3)}
  <text x="162" y="186" text-anchor="middle" fill="#e74c3c" font-size="12.5" font-family="Heebo,sans-serif" font-weight="900">אל תפשוט בגדים ואל תזיז את האבר</text>

  <text x="180" y="322" text-anchor="middle" fill="#7eb8f7" font-size="11.5" font-family="Heebo,sans-serif">הזזה מחמירה את הפגיעה</text>
`;


// ── אזורי שיט ──────────────────────────────────────────────────────────────
// Recovered from the hand-written html/ files of 2026-07-10 (commits d1bd5c6,
// 2fb0ae3, 54afe73). Those were authored directly into html/ rather than into
// this file, so the first regen.js run overwrote them with the generator's
// single generic zones diagram and every one of these questions started
// showing the same picture. Keeping them here means regen cannot lose them again.

// חוף שאינו מוכרז: שיט חופשי עד מייל, עד 5 קשר בנתיב לחוף
SCENES_QA['zones_undeclared_beach'] = `
<defs>
    <linearGradient id="szSea" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#041e3a"/><stop offset="45%" stop-color="#0c4a7a"/>
      <stop offset="75%" stop-color="#1a7a8a"/><stop offset="100%" stop-color="#2ab5a5"/>
    </linearGradient>
    <linearGradient id="szSand" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#c8a96a"/><stop offset="100%" stop-color="#dcc48a"/>
    </linearGradient>
    <marker id="szArr" viewBox="0 0 6 6" refX="3" refY="3" markerWidth="4" markerHeight="4" orient="auto-start-reverse">
      <path d="M0,0 L6,3 L0,6 Z" fill="#7eb8f7"/>
    </marker>
    <marker id="szArrO" viewBox="0 0 6 6" refX="3" refY="3" markerWidth="4" markerHeight="4" orient="auto-start-reverse">
      <path d="M0,0 L6,3 L0,6 Z" fill="#f39c12"/>
    </marker>
  </defs><rect width="360" height="310" fill="url(#szSea)"/><path d="M0,55 Q90,53 180,55 Q270,57 360,55" fill="none" stroke="#fff" stroke-width="0.5" opacity="0.06">
      <animate attributeName="d" values="M0,55 Q90,53 180,55 Q270,57 360,55;M0,57 Q90,59 180,57 Q270,54 360,57;M0,55 Q90,53 180,55 Q270,57 360,55" dur="5s" repeatCount="indefinite"/></path><path d="M0,100 Q90,98 180,100 Q270,102 360,100" fill="none" stroke="#fff" stroke-width="0.5" opacity="0.08">
      <animate attributeName="d" values="M0,100 Q90,98 180,100 Q270,102 360,100;M0,102 Q90,104 180,102 Q270,99 360,102;M0,100 Q90,98 180,100 Q270,102 360,100" dur="5s" repeatCount="indefinite"/></path><path d="M0,145 Q90,143 180,145 Q270,147 360,145" fill="none" stroke="#fff" stroke-width="0.5" opacity="0.10">
      <animate attributeName="d" values="M0,145 Q90,143 180,145 Q270,147 360,145;M0,147 Q90,149 180,147 Q270,144 360,147;M0,145 Q90,143 180,145 Q270,147 360,145" dur="5s" repeatCount="indefinite"/></path><path d="M0,190 Q90,188 180,190 Q270,192 360,190" fill="none" stroke="#fff" stroke-width="0.5" opacity="0.11">
      <animate attributeName="d" values="M0,190 Q90,188 180,190 Q270,192 360,190;M0,192 Q90,194 180,192 Q270,189 360,192;M0,190 Q90,188 180,190 Q270,192 360,190" dur="5s" repeatCount="indefinite"/></path><path d="M0,235 Q90,233 180,235 Q270,237 360,235" fill="none" stroke="#fff" stroke-width="0.5" opacity="0.13">
      <animate attributeName="d" values="M0,235 Q90,233 180,235 Q270,237 360,235;M0,237 Q90,239 180,237 Q270,234 360,237;M0,235 Q90,233 180,235 Q270,237 360,235" dur="5s" repeatCount="indefinite"/></path><path d="M0,280 Q90,278 180,280 Q270,282 360,280" fill="none" stroke="#fff" stroke-width="0.5" opacity="0.15">
      <animate attributeName="d" values="M0,280 Q90,278 180,280 Q270,282 360,280;M0,282 Q90,284 180,282 Q270,279 360,282;M0,280 Q90,278 180,280 Q270,282 360,280" dur="5s" repeatCount="indefinite"/></path><path d="M0,305 Q45,302 90,305 Q135,308 180,305 Q225,302 270,305 Q315,308 360,305" fill="none" stroke="#fff" stroke-width="1.8" opacity="0.5">
    <animate attributeName="d" values="M0,305 Q45,302 90,306 Q135,308 180,305 Q225,302 270,306 Q315,308 360,305;M0,307 Q45,309 90,307 Q135,304 180,307 Q225,310 270,307 Q315,304 360,307;M0,305 Q45,302 90,306 Q135,308 180,305 Q225,302 270,306 Q315,308 360,305" dur="3.5s" repeatCount="indefinite"/></path><rect x="0" y="305" width="360" height="115" fill="url(#szSand)"/><rect x="0" y="125" width="360" height="180" fill="#2980b9" opacity="0.06"/><line x1="20" y1="125" x2="340" y2="125" stroke="#fff" stroke-width="2.5" stroke-dasharray="10,5" opacity="0.85"/><line x1="30" y1="125" x2="30" y2="305" stroke="#7eb8f7" stroke-width="1.5" marker-start="url(#szArr)" marker-end="url(#szArr)"/><text x="36" y="211" fill="#7eb8f7" font-size="11" font-family="Heebo,sans-serif" font-weight="700">300</text><text x="36" y="225" fill="#7eb8f7" font-size="11" font-family="Heebo,sans-serif" font-weight="700">מטר</text><line x1="180" y1="300" x2="180" y2="130" stroke="#fff" stroke-width="2.5" stroke-dasharray="6,4" opacity="0.8"/><polygon points="180,130 175,140 185,140" fill="#fff" opacity="0.7"/><text x="188" y="255" fill="#fff" font-size="10" font-family="Heebo,sans-serif" opacity="0.9">ניצב לחוף</text><rect x="125" y="193" width="70" height="32" rx="6" fill="#0c1a3a" stroke="#f39c12" stroke-width="1.5" opacity="0.9"/><text x="160" y="209" text-anchor="middle" fill="#f39c12" font-size="13" font-family="Heebo,sans-serif" font-weight="900">עד 5 קשר</text><text x="160" y="223" text-anchor="middle" fill="#f39c12" font-size="10" font-family="Heebo,sans-serif">(9 קמ״ש)</text><text x="180" y="105" text-anchor="middle" fill="#2ecc71" font-size="13" font-family="Heebo,sans-serif" font-weight="700">שיט חופשי עד ל-1 מייל ⚓</text><g transform="translate(250,235) rotate(-15)">
    <ellipse rx="5" ry="12" fill="#2c3e50" stroke="#445"/><ellipse cy="-6" rx="3.5" ry="4" fill="#e74c3c"/>
    <circle cy="-1" r="2" fill="#f5d76e"/><path d="M-1.5,10 L0,16 L1.5,10" fill="#fff" opacity="0.5"/>
  </g><text x="180" y="335" text-anchor="middle" fill="#8a7040" font-size="12" font-family="Heebo,sans-serif" font-weight="700">חוף שאינו חוף רחצה</text><text x="180" y="20" text-anchor="middle" fill="#fff" font-size="14" font-family="Heebo,sans-serif" font-weight="900">אזורי שיט - חוף לא מוכרז</text><text x="180" y="38" text-anchor="middle" fill="#7eb8f7" font-size="11" font-family="Heebo,sans-serif">מבט מלמעלה (אווירי)</text>
`;

// שפך נחל הירקון: אסור לאופנוע ים לשוט בנחלים
SCENES_QA['zones_river_mouth'] = `
<defs>
      <linearGradient id="yrSea" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#7cbad6"/><stop offset="100%" stop-color="#a8d8ea"/>
      </linearGradient>
      <linearGradient id="yrRiver" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#6bafd4"/><stop offset="100%" stop-color="#4a90b8"/>
      </linearGradient>
    </defs><rect width="360" height="420" fill="#e8e0d0"/><path d="M0,0 L0,280 Q30,260 60,270 Q100,285 130,260 L160,180 Q180,130 210,100 L260,60 L360,0 Z" fill="url(#yrSea)"/><path d="M180,280 Q220,250 280,260 Q330,270 350,300 L350,370 Q300,380 240,370 Q200,360 180,340 Z" fill="#3a8a3a" opacity="0.6"/><text x="270" y="320" text-anchor="middle" fill="#1a5a1a" font-size="11" font-family="Heebo,sans-serif" font-weight="700">פארק הירקון</text><path d="M350,350 Q300,340 260,310 Q220,280 190,260 Q160,240 140,220 Q120,200 110,170 Q100,140 80,120" fill="none" stroke="#4a90b8" stroke-width="28" stroke-linecap="round"/><path d="M350,350 Q300,340 260,310 Q220,280 190,260 Q160,240 140,220 Q120,200 110,170 Q100,140 80,120" fill="none" stroke="#6bb8e0" stroke-width="20" stroke-linecap="round"/><text x="95" y="110" text-anchor="middle" fill="#1a5080" font-size="10" font-family="Heebo,sans-serif" font-weight="700">שפך</text><text x="260" y="295" fill="#fff" font-size="14" font-family="Heebo,sans-serif" font-weight="900">נחל הירקון</text><path d="M130,260 L130,420" stroke="#d4a830" stroke-width="5"/><path d="M0,350 L360,350" stroke="#999" stroke-width="3"/><path d="M160,180 L50,260" stroke="#d4a830" stroke-width="4"/><text x="260" y="30" fill="#555" font-size="10" font-family="Heebo,sans-serif">תחנת הכוח רדינג</text><rect x="245" y="40" width="30" height="20" fill="#888" opacity="0.4"/><rect x="0" y="300" width="40" height="50" fill="#5a7a9a" opacity="0.5"/><text x="20" y="330" text-anchor="middle" fill="#fff" font-size="8" font-family="Heebo,sans-serif">נמל ת״א</text><g transform="translate(180,170)"><circle r="32" fill="#e74c3c" stroke="#c0392b" stroke-width="3"/><circle r="24" fill="#fff"/><rect x="-20" y="-5" width="40" height="10" rx="2" fill="#e74c3c"/></g><line x1="180" y1="202" x2="180" y2="240" stroke="#555" stroke-width="3" stroke-linecap="round"/><text x="180" y="262" text-anchor="middle" fill="#e74c3c" font-size="16" font-family="Heebo,sans-serif" font-weight="900">אסור לאופנוע ים</text><text x="180" y="280" text-anchor="middle" fill="#e74c3c" font-size="14" font-family="Heebo,sans-serif" font-weight="700">לשוט בנחלים!</text><g transform="translate(180,140)" opacity="0.5"><line x1="-15" y1="-15" x2="15" y2="15" stroke="#e74c3c" stroke-width="3"/><line x1="15" y1="-15" x2="-15" y2="15" stroke="#e74c3c" stroke-width="3"/></g><g transform="translate(100,90) rotate(-30)">
    <ellipse rx="5" ry="12" fill="#2c3e50" stroke="#445"/><ellipse cy="-6" rx="3.5" ry="4" fill="#e74c3c"/>
    <circle cy="-1" r="2" fill="#f5d76e"/><path d="M-1.5,10 L0,16 L1.5,10" fill="#fff" opacity="0.5"/>
  </g><text x="40" y="50" fill="#1a5080" font-size="14" font-family="Heebo,sans-serif" font-weight="700">הים התיכון</text><text x="180" y="20" text-anchor="middle" fill="#333" font-size="15" font-family="Heebo,sans-serif" font-weight="900">שיט בנחלים - שפך הירקון</text>
`;

// חוף רחצה מוכרז: מבט אווירי עם הגבולות, אזורי החיץ ונתיב כלי השיט
SCENES_QA['zones_declared_beach'] = `
<defs>
    <linearGradient id="szSea" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#041e3a"/><stop offset="45%" stop-color="#0c4a7a"/>
      <stop offset="75%" stop-color="#1a7a8a"/><stop offset="100%" stop-color="#2ab5a5"/>
    </linearGradient>
    <linearGradient id="szSand" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#c8a96a"/><stop offset="100%" stop-color="#dcc48a"/>
    </linearGradient>
    <marker id="szArr" viewBox="0 0 6 6" refX="3" refY="3" markerWidth="4" markerHeight="4" orient="auto-start-reverse">
      <path d="M0,0 L6,3 L0,6 Z" fill="#7eb8f7"/>
    </marker>
    <marker id="szArrO" viewBox="0 0 6 6" refX="3" refY="3" markerWidth="4" markerHeight="4" orient="auto-start-reverse">
      <path d="M0,0 L6,3 L0,6 Z" fill="#f39c12"/>
    </marker>
  </defs><rect width="360" height="310" fill="url(#szSea)"/><path d="M0,55 Q90,53 180,55 Q270,57 360,55" fill="none" stroke="#fff" stroke-width="0.5" opacity="0.06">
      <animate attributeName="d" values="M0,55 Q90,53 180,55 Q270,57 360,55;M0,57 Q90,59 180,57 Q270,54 360,57;M0,55 Q90,53 180,55 Q270,57 360,55" dur="5s" repeatCount="indefinite"/></path><path d="M0,100 Q90,98 180,100 Q270,102 360,100" fill="none" stroke="#fff" stroke-width="0.5" opacity="0.08">
      <animate attributeName="d" values="M0,100 Q90,98 180,100 Q270,102 360,100;M0,102 Q90,104 180,102 Q270,99 360,102;M0,100 Q90,98 180,100 Q270,102 360,100" dur="5s" repeatCount="indefinite"/></path><path d="M0,145 Q90,143 180,145 Q270,147 360,145" fill="none" stroke="#fff" stroke-width="0.5" opacity="0.10">
      <animate attributeName="d" values="M0,145 Q90,143 180,145 Q270,147 360,145;M0,147 Q90,149 180,147 Q270,144 360,147;M0,145 Q90,143 180,145 Q270,147 360,145" dur="5s" repeatCount="indefinite"/></path><path d="M0,190 Q90,188 180,190 Q270,192 360,190" fill="none" stroke="#fff" stroke-width="0.5" opacity="0.11">
      <animate attributeName="d" values="M0,190 Q90,188 180,190 Q270,192 360,190;M0,192 Q90,194 180,192 Q270,189 360,192;M0,190 Q90,188 180,190 Q270,192 360,190" dur="5s" repeatCount="indefinite"/></path><path d="M0,235 Q90,233 180,235 Q270,237 360,235" fill="none" stroke="#fff" stroke-width="0.5" opacity="0.13">
      <animate attributeName="d" values="M0,235 Q90,233 180,235 Q270,237 360,235;M0,237 Q90,239 180,237 Q270,234 360,237;M0,235 Q90,233 180,235 Q270,237 360,235" dur="5s" repeatCount="indefinite"/></path><path d="M0,280 Q90,278 180,280 Q270,282 360,280" fill="none" stroke="#fff" stroke-width="0.5" opacity="0.15">
      <animate attributeName="d" values="M0,280 Q90,278 180,280 Q270,282 360,280;M0,282 Q90,284 180,282 Q270,279 360,282;M0,280 Q90,278 180,280 Q270,282 360,280" dur="5s" repeatCount="indefinite"/></path><path d="M0,305 Q45,302 90,305 Q135,308 180,305 Q225,302 270,305 Q315,308 360,305" fill="none" stroke="#fff" stroke-width="1.8" opacity="0.5">
    <animate attributeName="d" values="M0,305 Q45,302 90,306 Q135,308 180,305 Q225,302 270,306 Q315,308 360,305;M0,307 Q45,309 90,307 Q135,304 180,307 Q225,310 270,307 Q315,304 360,307;M0,305 Q45,302 90,306 Q135,308 180,305 Q225,302 270,306 Q315,308 360,305" dur="3.5s" repeatCount="indefinite"/></path><rect x="0" y="305" width="360" height="115" fill="url(#szSand)"/><rect x="82" y="125" width="196" height="180" fill="#e74c3c" opacity="0.07"/><rect x="49" y="125" width="33" height="180" fill="#f39c12" opacity="0.05"/><rect x="278" y="125" width="33" height="180" fill="#f39c12" opacity="0.05"/><line x1="49" y1="125" x2="311" y2="125" stroke="#fff" stroke-width="2.5" stroke-dasharray="10,5" opacity="0.85"/><line x1="82" y1="125" x2="82" y2="305" stroke="#e74c3c" stroke-width="2.5" stroke-dasharray="8,4" opacity="0.8"/><line x1="278" y1="125" x2="278" y2="305" stroke="#e74c3c" stroke-width="2.5" stroke-dasharray="8,4" opacity="0.8"/><line x1="49" y1="125" x2="49" y2="305" stroke="#f39c12" stroke-width="2" stroke-dasharray="7,4" opacity="0.7"/><line x1="311" y1="125" x2="311" y2="305" stroke="#f39c12" stroke-width="2" stroke-dasharray="7,4" opacity="0.7"/><line x1="34" y1="127" x2="34" y2="303" stroke="#7eb8f7" stroke-width="1.5" marker-start="url(#szArr)" marker-end="url(#szArr)"/><text x="34" y="215" text-anchor="middle" fill="#7eb8f7" font-size="10" font-family="Heebo,sans-serif" font-weight="700" transform="rotate(-90,34,215)">300 מטר מהחוף</text><line x1="51" y1="287" x2="80" y2="287" stroke="#f39c12" stroke-width="1.5" marker-start="url(#szArrO)" marker-end="url(#szArrO)"/><text x="65.5" y="282" text-anchor="middle" fill="#f39c12" font-size="10" font-family="Heebo,sans-serif" font-weight="700">50 מ׳</text><line x1="280" y1="287" x2="309" y2="287" stroke="#f39c12" stroke-width="1.5" marker-start="url(#szArrO)" marker-end="url(#szArrO)"/><text x="294.5" y="282" text-anchor="middle" fill="#f39c12" font-size="10" font-family="Heebo,sans-serif" font-weight="700">50 מ׳</text><rect x="80" y="301" width="4" height="14" rx="1" fill="#e74c3c"/><rect x="276" y="301" width="4" height="14" rx="1" fill="#e74c3c"/><rect x="174" y="321" width="12" height="12" rx="1" fill="#8B4513" stroke="#6B3310" stroke-width="0.5"/><circle cx="180" cy="327" r="10" fill="#e74c3c" opacity="0.5"/><circle cx="180" cy="327" r="10" fill="none" stroke="#c0392b" stroke-width="1"/><line x1="180" y1="317" x2="180" y2="337" stroke="#8B4513" stroke-width="1.5"/><text x="180" y="345" text-anchor="middle" fill="#6B3310" font-size="9" font-family="Heebo,sans-serif" font-weight="700">סוכת מציל</text><text x="180" y="361" text-anchor="middle" fill="#7a6030" font-size="11" font-family="Heebo,sans-serif" font-weight="700">חוף רחצה מוכרז</text><line x1="86" y1="371" x2="172" y2="371" stroke="#9a8050" stroke-width="1" marker-start="url(#szArrO)" marker-end="url(#szArrO)"/><text x="131" y="383" text-anchor="middle" fill="#9a8050" font-size="9" font-family="Heebo,sans-serif">150 מ׳</text><line x1="188" y1="371" x2="274" y2="371" stroke="#9a8050" stroke-width="1" marker-start="url(#szArrO)" marker-end="url(#szArrO)"/><text x="229" y="383" text-anchor="middle" fill="#9a8050" font-size="9" font-family="Heebo,sans-serif">150 מ׳</text><circle cx="150" cy="293" r="2" fill="#f5d76e" opacity="0.6"/><circle cx="190" cy="287" r="2" fill="#f5d76e" opacity="0.6"/><circle cx="125" cy="297" r="2" fill="#f5d76e" opacity="0.6"/><circle cx="220" cy="291" r="2" fill="#f5d76e" opacity="0.6"/><circle cx="180" cy="281" r="2" fill="#f5d76e" opacity="0.6"/><circle cx="58.5" cy="150" r="3" fill="#f39c12" stroke="#e67e22" stroke-width="0.8"/><circle cx="72.5" cy="150" r="3" fill="#f39c12" stroke="#e67e22" stroke-width="0.8"/><circle cx="58.5" cy="190" r="3" fill="#f39c12" stroke="#e67e22" stroke-width="0.8"/><circle cx="72.5" cy="190" r="3" fill="#f39c12" stroke="#e67e22" stroke-width="0.8"/><circle cx="58.5" cy="230" r="3" fill="#f39c12" stroke="#e67e22" stroke-width="0.8"/><circle cx="72.5" cy="230" r="3" fill="#f39c12" stroke="#e67e22" stroke-width="0.8"/><circle cx="58.5" cy="270" r="3" fill="#f39c12" stroke="#e67e22" stroke-width="0.8"/><circle cx="72.5" cy="270" r="3" fill="#f39c12" stroke="#e67e22" stroke-width="0.8"/><text x="65.5" y="139" text-anchor="middle" fill="#f39c12" font-size="9" font-family="Heebo,sans-serif" font-weight="700">נתיב כלי שיט</text><g transform="translate(333,215) rotate(-20)">
    <ellipse rx="5" ry="12" fill="#2c3e50" stroke="#445"/><ellipse cy="-6" rx="3.5" ry="4" fill="#e74c3c"/>
    <circle cy="-1" r="2" fill="#f5d76e"/><path d="M-1.5,10 L0,16 L1.5,10" fill="#fff" opacity="0.5"/>
  </g><rect x="8" y="45" width="8" height="8" fill="#e74c3c" opacity="0.25" stroke="#e74c3c" stroke-width="0.5"/><text x="20" y="53" fill="#e74c3c" font-size="9" font-family="Heebo,sans-serif">אסור לשיט</text><rect x="8" y="58" width="8" height="8" fill="#f39c12" opacity="0.25" stroke="#f39c12" stroke-width="0.5"/><text x="20" y="66" fill="#f39c12" font-size="9" font-family="Heebo,sans-serif">אזור חיץ 50 מ׳</text><circle cx="12" cy="77" r="3" fill="#f39c12" stroke="#e67e22" stroke-width="0.6"/><text x="20" y="80" fill="#f39c12" font-size="9" font-family="Heebo,sans-serif">מצוף</text><text x="180" y="20" text-anchor="middle" fill="#fff" font-size="14" font-family="Heebo,sans-serif" font-weight="900">אזורי שיט - חוף רחצה מוכרז</text><text x="180" y="38" text-anchor="middle" fill="#7eb8f7" font-size="11" font-family="Heebo,sans-serif">מבט מלמעלה (אווירי)</text>
`;

function getScene(topic, qText) {
  const q = qText || '';
  if(/\([A-P]\)/.test(q) || /(?:כלי.(?:ה)?שייט|אופנוע.{0,3}ים|מפרשית)\s+[""״"(]?([A-P])\b/.test(q)) {
    const compass = generateCompassRoseScene(q);
    if (compass) return compass;
  }
  if(topic==='אזורי שיט') {
    // "חוף שאינו חוף רחצה מוכרז" contains מוכרז, so the negation has to be
    // tested first or every non-declared-beach question lands on the declared
    // beach diagram.
    const negated = /שאינו|שאיננו|לא מוכרז/.test(q);
    if(/נחל|שפך/.test(q))                            return SCENES_QA['zones_river_mouth'];
    if(!negated && /חוף רחצה|מוכרז/.test(q))          return SCENES_QA['zones_declared_beach'];
    if(negated || /200 מטר/.test(q))                  return SCENES_QA['zones_undeclared_beach'];
    // open sea, closed areas, Dead Sea, Eilat keep the general zones scene
  }
  if(topic==='תמרוני ספינה') {
    // The two towing families share the word גרירה, so the craft-on-craft case
    // has to be claimed by its own wording before the skier catch-all.
    if(/חבל גרירה|גרירת אופנוע ים ע|לקשור/.test(q))         return SCENES_QA['tow_craft'];
    if(/סקי|בננה|לגרור/.test(q))                             return SCENES_QA['tow_skier'];
    if(/התהפך|לישר/.test(q))                                 return SCENES_QA['right_capsized'];
    if(/החפה|בין שני גלים/.test(q))                          return SCENES_QA['beaching'];
  }
  if(topic==='עזרה ראשונה') {
    if(/מדוזה|צריב/.test(q))                       return SCENES_QA['firstaid_jellyfish'];
    if(/מכת חום|חום.*נפגע|צל/.test(q))              return SCENES_QA['firstaid_heatstroke'];
    if(/שבר|גפ/.test(q))                            return SCENES_QA['firstaid_fracture'];
    if(/טבע|הנשמה.*אינו נושם|מריאות/.test(q))       return SCENES_QA['firstaid_drowning'];
    if(/מחוסר הכרה|דופק|נשימה/.test(q))             return SCENES_QA['firstaid_abc'];
  }
  if(topic==='סכנות רכיבה ותמרון') {
    // Order matters: the wave and approach questions also mention speed and
    // danger, so they have to be claimed before the rider-risk catch-all.
    if(/גלי חוף|מעבר.*גל|לאחר מעבר/.test(q))              return SCENES_QA['pwc_wave_launch'];
    if(/מהצד|התהפכות|גלים גבוהים/.test(q))                 return SCENES_QA['pwc_beam_capsize'];
    if(/גישה לכלי|להתקרב|לעצור לידו|מהירות איטית|למנוע גלים|ליד כלי/.test(q))
                                                            return SCENES_QA['pwc_slow_approach'];
    if(/נוסע מאחור|האצה|מדומם|אחיזה|נתון לסכנה/.test(q))   return SCENES_QA['pwc_rider_risk'];
  }
  if(topic==='זכות מעבר' && /מפרש|sail/i.test(q)) return SCENES['זכות_מעבר_מפרש'];
  if(/VHF|רדיו|קשר/.test(topic)) return SCENES['קשר VHF'];
  if(/מכ.מ|radar/i.test(topic)) return SCENES['מכ"מ'];

  if(topic==='ניווט') {
    if(/מרחק|קנה.מידה|מדיד.*מרקטור|מרקטור.*מדיד/.test(q))  return SCENES_QA['mercator_distance'];
    if(/כוכב הצפון|פולר|polaris/i.test(q))                   return SCENES_QA['polaris'];
    if(/זרח|שוקע|שמש.*זורח|rise.*east/i.test(q))             return SCENES_QA['earth_rotation'];
    if(/סובב|סיבוב|מסתובב/.test(q))                          return SCENES_QA['earth_rotation'];
    if(/מי?יל ימי|nautical mile|1852|דקת קשת/.test(q))          return SCENES_QA['nautical_mile'];
    if(/5 שניות|15 מטר|5.83|מהירות.*שניות|שניות.*מהירות/.test(q)) return SCENES_QA['speed_calc'];
    if(/אופק.*מרחק|מרחק.*אופק|גובה.*מטר/.test(q))             return SCENES_QA['horizon_dist'];
    if(/זמן מקומי|local time|קו האורך.*זמן/.test(q))           return SCENES_QA['local_time'];
    if(/zone time|אזור זמן|7.5|15 מעלות.*זמן/.test(q))         return SCENES_QA['zone_time'];
    if(/UTC\+3|\+3.*זמן|זמן.*\+3/.test(q))                     return SCENES_QA['utc_plus3'];
    if(/utc|הגדרת.*זמן|UTC.*שווה|מתואם/i.test(q))              return SCENES_QA['utc_def'];
    if(/31 דצמבר|179°|קו.*תאריך|תאריך.*קו/.test(q))             return SCENES_QA['date_line'];
    if(/עומד|לא.*תנועה|not moving|אינה.*זז/.test(q))            return SCENES_QA['wind_stationary'];
    if(/מד הרוח.*הפלג|הפלג.*מד הרוח|apparent|יחסית.*הפלג/.test(q)) return SCENES_QA['apparent_wind'];
    if(/קורס מגנטי|magnetic course/.test(q))                   return SCENES_QA['magnetic_course'];
    if(/rhumb|ריים/.test(q))                                    return SCENES_QA['rhumb_line'];
    if(/עונות|23.5|תנועה.*שמש.*מעגל|ציר.*נטו/.test(q))          return SCENES_QA['seasons'];
    if(/ירח.*גאות|גאות.*ירח|גאות.*שפל.*ירח/.test(q))           return SCENES_QA['tides'];
    if(/קווי רוחב.*מעגל|parallel|מעגלים.*קטנים/.test(q))       return SCENES_QA['latitude_lines'];
    if(/קווי אורך.*מעגל|meridian|מעגלים.*גדולים/.test(q))      return SCENES_QA['longitude_lines'];
    if(/90 מעלות|קוטב.*מעלות|מעלות.*קוטב/.test(q))              return SCENES_QA['poles_90'];
    if(/גרינוויץ|greenwich|קו.*ראשוני|ראשוני.*קו/.test(q))      return SCENES_QA['greenwich'];
    if(/חולקה|חיתוך|חיתך|נקודות חיתוך/.test(q))                return SCENES_QA['geo_grid'];
  }

  if(topic==='אורות ניווט') {
    if(/גרירה|טרולר|trawl/i.test(q))                           return SCENES_QA['lights_trawler'];
    if(/ללא שליטה|not under command/i.test(q))                  return SCENES_QA['lights_nuc'];
    if(/מוגבל בכושר|restricted.*maneuve/i.test(q))             return SCENES_QA['lights_ram'];
    if(/עוגנת|at anchor/i.test(q))                              return SCENES_QA['lights_anchor'];
    if(/שרטון|aground/i.test(q))                                return SCENES_QA['lights_aground'];
    if(/פיילוט|pilot/i.test(q))                                 return SCENES_QA['lights_pilot'];
    if(/סופת|מינסוויפר|minesweep/i.test(q))                    return SCENES_QA['lights_minesweeper'];
    if(/גורר|towing/i.test(q))                                  return SCENES_QA['lights_towing'];
    if(/מפרש|sail/i.test(q))                                    return SCENES_QA['lights_sailing'];
    if(/112\.5|קשת.*ירוק|ירוק.*קשת|אור הצד|אור.*צד.*ימין/i.test(q)) return SCENES_QA['lights_arc_green'];
    if(/50 מטר|מעל 50|over 50/i.test(q))                       return SCENES_QA['lights_large'];
    if(/אור גב|אור ירכתיים|stern light/i.test(q))                return SCENES_QA['lights_stern'];
    if(/מתחת.{0,3}7|under 7/i.test(q))                         return SCENES_QA['lights_small'];
    if(/מוגבל בשוקע|constrained.*draft/i.test(q))              return SCENES_QA['lights_constrained'];
    if(/225|ראש.תורן.*קשת|קשת.*ראש.תורן/i.test(q))            return SCENES_QA['lights_masthead_225'];
    if(/טווח נראות|visibility range|טווח.*ראש/i.test(q))       return SCENES_QA['lights_visibility'];
    if(/מתי.*חייב|מתי.*להדליק|when.*required|שקיע/i.test(q))  return SCENES_QA['lights_when'];
    if(/ירוק בלבד|only green|ממרחק/i.test(q))                  return SCENES_QA['lights_see_green'];
    if(/שני.*לבנ.*אחד מעל|two white/i.test(q))                 return SCENES_QA['lights_two_whites'];
    if(/אדום מעל לבן|red.*over.*white/i.test(q))               return SCENES_QA['lights_red_over_white'];
    if(/שני.*אדומ.*אורות צד|NUC.*דרכה|ללא שליטה.*עושה/i.test(q)) return SCENES_QA['lights_nuc_making_way'];
    if(/ממוכנת.*דרכה|power.*underway/i.test(q))                return SCENES_QA['lights_power'];
    return SCENES_QA['lights_power'];
  }

  if(topic==='דגלים') return generateFlagScene(q);

  if(topic==='ספנות') {
    if(/נפל לים|man overboard|\bMOB\b|אדם בים|אדם שנפל/i.test(q))  return SCENES_QA['mob_approach'];
    return SCENES['ספנות'];
  }

  return SCENES[topic] || SCENES['ניווט'];
}

function letterToIdx(l) {
  return {א:0,ב:1,ג:2,ד:3,a:0,b:1,c:2,d:3}[l?.trim()] ?? 0;
}

function parseBlastPattern(t) {
  t = t || '';
  const blasts = [];
  const nMap = {'אחת':1,'אחד':1,'שתי':2,'שתיים':2,'שני':2,'שלוש':3,'שלושה':3,'ארבע':4,'חמש':5,'חמישה':5};
  const toN = s => nMap[s] || parseInt(s) || 1;
  let m;
  m = t.match(/(\d+|אחת?|שת[יים]*|שני|שלוש[ה]?|ארבע|חמש[ה]?)\s*ארוכ[ות]+\s*\+\s*(\d+|אחת?|שת[יים]*|שני|שלוש[ה]?)\s*קצר[ות]+/);
  if(m){ for(let i=0;i<toN(m[1]);i++) blasts.push('L'); for(let i=0;i<toN(m[2]);i++) blasts.push('S'); return blasts; }
  m = t.match(/ארוכה\s*\+\s*(\d+|אחת?|שת[יים]*|שני)\s*קצר[ות]+/);
  if(m){ blasts.push('L'); for(let i=0;i<toN(m[1]);i++) blasts.push('S'); return blasts; }
  m = t.match(/(\d+|חמש[ה]?|ארבע|שלוש[ה]?|שת[יים]*|שני|אחת?)\s*(?:צפירות?\s*)?קצר[ות]+/);
  if(m){ for(let i=0;i<toN(m[1]);i++) blasts.push('S'); return blasts; }
  m = t.match(/(\d+|אחת?|שת[יים]*|שני|שלוש[ה]?|ארבע)\s*(?:צפירות?\s*)?ארוכ[ות]+/);
  if(m){ for(let i=0;i<toN(m[1]);i++) blasts.push('L'); return blasts; }
  if(/צפירה ארוכה/.test(t)) return ['L'];
  return null; // no match
}

function parseBlastOverrideStr(str) {
  if(!str || !str.trim()) return null;
  str = str.trim().toUpperCase();
  // Expand shorthand like "2L+1S" or "2L 3S"
  str = str.replace(/(\d+)\s*L/g, (_, n) => ('L ').repeat(parseInt(n)).trim());
  str = str.replace(/(\d+)\s*S/g, (_, n) => ('S ').repeat(parseInt(n)).trim());
  str = str.replace(/[+,]/g, ' ');
  const parts = str.split(/\s+/).filter(p => p === 'L' || p === 'S');
  return parts.length ? parts : null;
}

function parseBlastPatternMulti(answerText, questionText, explText, override) {
  if(override) { const r = parseBlastOverrideStr(override); if(r) return r; }
  return parseBlastPattern(answerText)
      || parseBlastPattern(questionText)
      || parseBlastPattern(explText)
      || ['L'];
}

const BLAST_DUR = { L: 2.0, S: 1.0 };
const BLAST_GAP = 1.0;

// ── Boat drawing helpers ─────────────────────────────────────────────────────
function sideJetSki(cx, by, color, dk, s) {
  // Personal watercraft, bow→right, by=waterline. s scales around (cx,by).
  color = color || '#f1c40f'; dk = dk || '#c8a000'; s = s || 1;
  const p = (x, y) => `${cx + x * s},${by + y * s}`;
  // Proportions measured off a side-on photo of a runabout PWC, normalised to
  // a 100-unit length: deep hull, tall lifted bow, long saddle, and handlebars
  // forward of centre with the storage hood ahead of them.
  return `
  <g>
  <!-- Stern boarding platform -->
  <path d="M${p(-57,-1)} L${p(-44,-3)} L${p(-44,3)} L${p(-55,2)} Z" fill="${dk}" opacity=".85"/>
  <!-- Hull: deck line aft, rising to a tall bow, keel sweeping up at both ends -->
  <path d="M${p(-46,-8)} L${p(34,-8)} Q${p(47,-9)} ${p(50,-13)}
           Q${p(51,-3)} ${p(43,3)} Q${p(26,8)} ${p(-6,8)}
           Q${p(-32,8)} ${p(-42,3)} Z"
        fill="${color}" stroke="${dk}" stroke-width="${1.6 * s}" stroke-linejoin="round"/>
  <!-- Waterline shading on the submerged part -->
  <path d="M${p(-43,0)} L${p(46,0)} Q${p(26,8)} ${p(-6,8)} Q${p(-32,8)} ${p(-42,3)} Z"
        fill="${dk}" opacity=".45"/>
  <!-- Rubbing strake along the hull -->
  <path d="M${p(-45,-4)} L${p(44,-5)}" stroke="${dk}" stroke-width="${1.5 * s}" opacity=".8"/>
  <!-- Saddle: long, from the stern deck forward to the console -->
  <path d="M${p(-40,-8)} Q${p(-40,-15)} ${p(-34,-18)} Q${p(-22,-21)} ${p(-8,-20)}
           Q${p(3,-19)} ${p(10,-14)} L${p(12,-8)} Z"
        fill="#2c3e50" stroke="#1a2530" stroke-width="${1.3 * s}" stroke-linejoin="round"/>
  <!-- Front hood / storage, ahead of the rider, sloping to the bow -->
  <path d="M${p(10,-14)} L${p(12,-21)} Q${p(20,-23)} ${p(30,-21)} Q${p(41,-19)} ${p(47,-12)}
           L${p(46,-9)} Q${p(30,-11)} ${p(11,-12)} Z"
        fill="${color}" stroke="${dk}" stroke-width="${1.4 * s}" stroke-linejoin="round"/>
  <path d="M${p(30,-20)} Q${p(40,-18)} ${p(45,-13)}" fill="none" stroke="#fff" stroke-width="${1.6 * s}" opacity=".35"/>
  <!-- Handlebars, sitting just aft of the hood -->
  <path d="M${p(11,-26)} L${p(11,-17)}" stroke="#2c3e50" stroke-width="${2.4 * s}"/>
  <path d="M${p(4,-26)} L${p(17,-27)}" stroke="#2c3e50" stroke-width="${3 * s}" stroke-linecap="round"/>
  <circle cx="${cx + 3 * s}" cy="${by + -26 * s}" r="${2.6 * s}" fill="#1a2530"/>
  <circle cx="${cx + 18 * s}" cy="${by + -27 * s}" r="${2.6 * s}" fill="#1a2530"/>
  <!-- Jet nozzle -->
  <rect x="${cx + -50 * s}" y="${by + -6 * s}" width="${7 * s}" height="${7 * s}" rx="${1.5 * s}" fill="#7f8c8d"/>
  </g>`;
}

function topJetSki(cx, cy, s, color, dk, heading) {
  // PWC from above, bow→right by default. heading rotates it about (cx,cy).
  // Towing questions are all about the geometry between two craft, which a
  // profile view cannot show.
  s = s || 1; color = color || '#f1c40f'; dk = dk || '#c8a000';
  const p = (x, y) => `${cx + x * s},${cy + y * s}`;
  return `
  <g transform="rotate(${heading || 0},${cx},${cy})">
  <path d="M${p(46,0)} Q${p(30,-13)} ${p(4,-15)} L${p(-34,-14)} Q${p(-44,-12)} ${p(-46,0)}
           Q${p(-44,12)} ${p(-34,14)} L${p(4,15)} Q${p(30,13)} ${p(46,0)} Z"
        fill="${color}" stroke="${dk}" stroke-width="${1.6 * s}" stroke-linejoin="round"/>
  <ellipse cx="${cx - 8 * s}" cy="${cy}" rx="${20 * s}" ry="${9 * s}" fill="#2c3e50"/>
  <path d="M${p(16,-8)} L${p(16,8)}" stroke="#2c3e50" stroke-width="${3 * s}" stroke-linecap="round"/>
  <path d="M${p(-46,-5)} L${p(-52,0)} L${p(-46,5)} Z" fill="#7f8c8d"/>
  </g>`;
}

function lyingPerson(cx, cy, s, kit) {
  // Casualty supine, head to the left, lying on the line cy. Every first-aid
  // question here is about what you do to someone in this position.
  s = s || 1; kit = kit || '#e67e22';
  const p = (x, y) => `${cx + x * s},${cy + y * s}`;
  return `
  <g>
  <path d="M${p(4,-7)} L${p(46,-5)}" stroke="#2c3e50" stroke-width="${11 * s}" stroke-linecap="round"/>
  <path d="M${p(-30,-9)} L${p(6,-8)}" stroke="${kit}" stroke-width="${17 * s}" stroke-linecap="round"/>
  <path d="M${p(-18,-5)} L${p(0,3)}" stroke="${kit}" stroke-width="${6 * s}" stroke-linecap="round"/>
  <circle cx="${cx - 42 * s}" cy="${cy - 11 * s}" r="${9.5 * s}" fill="#f5cba7"/>
  </g>`;
}

function tick(x, y, s) {
  s = s || 1;
  return `<path d="M${x - 5 * s},${y} L${x - 1 * s},${y + 4 * s} L${x + 6 * s},${y - 5 * s}"
    fill="none" stroke="#2ecc71" stroke-width="${3 * s}" stroke-linecap="round" stroke-linejoin="round"/>`;
}

function cross(x, y, s) {
  s = s || 1;
  return `<g stroke="#e74c3c" stroke-width="${3 * s}" stroke-linecap="round">
    <path d="M${x - 5 * s},${y - 5 * s} L${x + 5 * s},${y + 5 * s}"/>
    <path d="M${x + 5 * s},${y - 5 * s} L${x - 5 * s},${y + 5 * s}"/></g>`;
}

function sternJetSki(cx, by, s, kit) {
  // Same craft seen end-on, rider aboard. A profile view cannot show roll, so
  // beam-sea capsize needs this one. Drawn upright around (cx,by)=waterline
  // centre; the caller wraps it in a rotate() to lean it over.
  s = s || 1; kit = kit || '#2980b9';
  const p = (x, y) => `${cx + x * s},${by + y * s}`;
  return `
  <g>
  <!-- hull below the waterline -->
  <path d="M${p(-32,-8)} L${p(32,-8)} Q${p(29,12)} ${p(0,17)} Q${p(-29,12)} ${p(-32,-8)} Z"
        fill="#c8a000" stroke="#8a7000" stroke-width="${1.6 * s}" stroke-linejoin="round"/>
  <!-- deck / gunwales -->
  <path d="M${p(-34,-8)} L${p(34,-8)} L${p(30,-18)} L${p(-30,-18)} Z"
        fill="#f1c40f" stroke="#c8a000" stroke-width="${1.6 * s}" stroke-linejoin="round"/>
  <!-- saddle -->
  <rect x="${cx - 13 * s}" y="${by - 25 * s}" width="${26 * s}" height="${8 * s}"
        rx="${3 * s}" fill="#2c3e50"/>
  <!-- handlebars seen end-on -->
  <path d="M${p(-15,-34)} L${p(15,-34)}" stroke="#2c3e50" stroke-width="${3 * s}" stroke-linecap="round"/>
  <!-- rider: torso, arms out to the bars, helmeted head. Kept tall relative to
       the hull — at true end-on proportions the figure reads as a stub. -->
  <path d="M${p(0,-26)} L${p(0,-50)}" stroke="${kit}" stroke-width="${14 * s}" stroke-linecap="round"/>
  <path d="M${p(0,-44)} L${p(-15,-35)}" stroke="${kit}" stroke-width="${5.5 * s}" stroke-linecap="round"/>
  <path d="M${p(0,-44)} L${p(15,-35)}" stroke="${kit}" stroke-width="${5.5 * s}" stroke-linecap="round"/>
  <path d="M${p(0,-29)} L${p(0,-47)}" stroke="#f4d03f" stroke-width="${10 * s}" stroke-linecap="round" opacity=".92"/>
  <circle cx="${cx}" cy="${by - 60 * s}" r="${9.5 * s}" fill="#f5cba7"/>
  <path d="M${p(-9.5,-61)} A${9.5*s},${9.5*s} 0 0 1 ${p(9.5,-61)} L${p(9.5,-64)} L${p(-9.5,-64)} Z" fill="${kit}"/>
  </g>`;
}

function sideRider(hx, hy, s, pose, kit) {
  // Seated rider in profile, facing right, drawn from the hip point (hx,hy) so
  // it drops straight onto a sideJetSki saddle. Two poses carry the whole
  // rider-risk topic: 'grip' is braced against the handlebars, 'thrown' has
  // lost the seat, which is the difference the questions turn on.
  s = s || 1; kit = kit || '#e67e22';
  const p = (x, y) => `${hx + x * s},${hy + y * s}`;
  const thrown = pose === 'thrown';
  // Thrown rider pivots back off the saddle: torso reclined, arms up, legs loose.
  const sh   = thrown ? [-13, -25] : [5, -26];   // shoulder
  const head = thrown ? [-21, -34] : [9, -34];   // head centre
  const hand = thrown ? [-3, -40]  : [20, -6];   // hands (bar grips sit low and forward)
  const knee = thrown ? [11, -7]   : [16, -2];
  const foot = thrown ? [22, 2]    : [17, 12];
  return `
  <g>
  <!-- rear leg, drawn first so the torso overlaps it -->
  <path d="M${p(0,-2)} L${p(knee[0]-2,knee[1]+1)} L${p(foot[0]-2,foot[1])}"
        fill="none" stroke="#1f2f3f" stroke-width="${6.5 * s}" stroke-linecap="round" stroke-linejoin="round" opacity=".75"/>
  <!-- torso -->
  <path d="M${p(0,-2)} L${p(sh[0],sh[1])}" fill="none" stroke="${kit}"
        stroke-width="${13 * s}" stroke-linecap="round"/>
  <!-- lifejacket over the torso, kept narrower than the torso so the kit colour
       still reads at the edges — the kit is what tells the two riders apart -->
  <path d="M${p(-1,-9)} L${p(sh[0]*0.85,sh[1]+3)}" fill="none" stroke="#f4d03f"
        stroke-width="${8 * s}" stroke-linecap="round" opacity=".92"/>
  <!-- front leg -->
  <path d="M${p(0,-2)} L${p(knee[0],knee[1])} L${p(foot[0],foot[1])}"
        fill="none" stroke="#2c3e50" stroke-width="${7 * s}" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- arm reaching for the bars, or flung up -->
  <path d="M${p(sh[0],sh[1])} L${p(hand[0],hand[1])}" fill="none" stroke="${kit}"
        stroke-width="${5.5 * s}" stroke-linecap="round"/>
  <!-- head, helmet and visor -->
  <circle cx="${hx + head[0] * s}" cy="${hy + head[1] * s}" r="${7.5 * s}" fill="#f5cba7"/>
  <path d="M${p(head[0]-8,head[1]-1)} A${8*s},${8*s} 0 0 1 ${p(head[0]+8,head[1]-1)} L${p(head[0]+8,head[1]-3)} L${p(head[0]-8,head[1]-3)} Z"
        fill="${kit}" opacity=".95"/>
  <circle cx="${hx + head[0] * s}" cy="${hy + (head[1] - 1) * s}" r="${8 * s}"
          fill="none" stroke="${kit}" stroke-width="${3 * s}" stroke-dasharray="${25 * s} ${100 * s}"/>
  </g>`;
}

function sideBoat(cx, by, color, dk) {
  // Pilothouse motorboat, bow→right, stern (motor)→left. by=waterline.
  return `
  <!-- Hull body -->
  <path d="M${cx-118},${by-4} L${cx-118},${by-16} L${cx-105},${by-20}
           L${cx+70},${by-20} L${cx+112},${by-6} L${cx+118},${by+2}
           L${cx-118},${by+2} Z" fill="${color}" stroke="${dk}" stroke-width="1.5"/>
  <!-- Hull keel/bottom -->
  <path d="M${cx-118},${by+2} L${cx+118},${by+2} L${cx+108},${by+14} L${cx-128},${by+14} Z"
        fill="${color}" stroke="${dk}" stroke-width="1.2" opacity=".85"/>
  <!-- Waterline stripe -->
  <line x1="${cx-118}" y1="${by+2}" x2="${cx+118}" y2="${by+2}" stroke="${dk}" stroke-width="1.8"/>
  <!-- Pilothouse / cabin -->
  <rect x="${cx-60}" y="${by-56}" width="106" height="38" rx="5" fill="${color}" stroke="${dk}" stroke-width="1.3"/>
  <!-- Cabin roof -->
  <rect x="${cx-56}" y="${by-66}" width="98" height="14" rx="6" fill="${dk}"/>
  <!-- Windshield (angled glass, bow side) -->
  <path d="M${cx+46},${by-56} L${cx+44},${by-66} L${cx+58},${by-66} L${cx+62},${by-56} Z"
        fill="#7eb8f7" opacity=".6" stroke="${dk}" stroke-width="0.8"/>
  <!-- Cabin windows -->
  <rect x="${cx-40}" y="${by-53}" width="20" height="13" rx="2.5" fill="#7eb8f7" opacity=".8"/>
  <rect x="${cx-14}" y="${by-53}" width="20" height="13" rx="2.5" fill="#7eb8f7" opacity=".8"/>
  <rect x="${cx+12}" y="${by-53}" width="20" height="13" rx="2.5" fill="#7eb8f7" opacity=".8"/>
  <!-- Bow deck (open, forward of cabin) -->
  <rect x="${cx+62}" y="${by-20}" width="46" height="14" rx="2" fill="${color}" stroke="${dk}" stroke-width="0.8" opacity=".9"/>
  <!-- Bow cleat -->
  <circle cx="${cx+96}" cy="${by-13}" r="3" fill="${dk}"/>
  <!-- Outboard motor at stern -->
  <rect x="${cx-135}" y="${by-30}" width="18" height="36" rx="3" fill="${dk}"/>
  <rect x="${cx-143}" y="${by-24}" width="10" height="22" rx="2" fill="${dk}"/>
  <!-- Motor prop/exhaust -->
  <path d="M${cx-136},${by+6} L${cx-152},${by+10} L${cx-150},${by+16} L${cx-134},${by+12} Z" fill="${dk}"/>
  <!-- Antenna on roof -->
  <line x1="${cx-30}" y1="${by-66}" x2="${cx-30}" y2="${by-86}" stroke="${dk}" stroke-width="1.5"/>
  <line x1="${cx-34}" y1="${by-86}" x2="${cx-26}" y2="${by-86}" stroke="${dk}" stroke-width="1"/>`;
}

function topBoat(cx, cy, color, dk, label) {
  // Top-view motorboat (bird's eye). Points right (bow→right).
  return `
  <!-- Hull -->
  <path d="M${cx+58},${cy} L${cx+20},${cy-15} L${cx-46},${cy-16} L${cx-58},${cy} L${cx-46},${cy+16} L${cx+20},${cy+15} Z"
        fill="${color}" stroke="${dk}" stroke-width="1.5"/>
  <!-- Cabin top -->
  <rect x="${cx-30}" y="${cy-10}" width="48" height="20" rx="4" fill="${dk}" opacity=".85"/>
  <!-- Windshield strip -->
  <rect x="${cx+18}" y="${cy-8}" width="14" height="16" rx="2" fill="#7eb8f7" opacity=".6"/>
  <!-- Bow point -->
  <polygon points="${cx+60},${cy} ${cx+50},${cy-6} ${cx+50},${cy+6}" fill="${dk}"/>
  <!-- Motor at stern -->
  <rect x="${cx-66}" y="${cy-6}" width="12" height="12" rx="2" fill="${dk}"/>
  <text x="${cx}" y="${cy+30}" text-anchor="middle" fill="${color}" font-size="9" font-family="Heebo,sans-serif" font-weight="700">${label}</text>`;
}

// ── Maritime Signal Flags ────────────────────────────────────────────────────
const SIGNAL_FLAGS = {
  Q: { name: 'Quebec', color: '#f1c40f', draw: (x,y,w,h) =>
    `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="#f1c40f"/>` },
  O: { name: 'Oscar', color: '#e74c3c', draw: (x,y,w,h) =>
    `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="#f1c40f"/>
     <polygon points="${x},${y} ${x+w},${y} ${x},${y+h}" fill="#e74c3c"/>` },
  A: { name: 'Alpha', color: '#2980b9', draw: (x,y,w,h) => {
    const notch = w*0.2;
    return `<polygon points="${x},${y} ${x+w},${y} ${x+w-notch},${y+h/2} ${x+w},${y+h} ${x},${y+h}" fill="white"/>
     <polygon points="${x+w/2},${y} ${x+w},${y} ${x+w-notch},${y+h/2} ${x+w},${y+h} ${x+w/2},${y+h}" fill="#2980b9"/>`;
  }},
  B: { name: 'Bravo', color: '#e74c3c', draw: (x,y,w,h) => {
    const notch = w*0.2;
    return `<polygon points="${x},${y} ${x+w},${y} ${x+w-notch},${y+h/2} ${x+w},${y+h} ${x},${y+h}" fill="#e74c3c"/>`;
  }},
  N: { name: 'November', color: '#2c3e50', draw: (x,y,w,h) => {
    const cw=w/4, ch=h/4;
    let svg = `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="white"/>`;
    for(let r=0;r<4;r++) for(let c=0;c<4;c++)
      if((r+c)%2===0) svg+=`<rect x="${x+c*cw}" y="${y+r*ch}" width="${cw}" height="${ch}" fill="#2c3e50"/>`;
    return svg;
  }},
  V: { name: 'Victor', color: '#e74c3c', draw: (x,y,w,h) =>
    `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="white"/>
     <line x1="${x}" y1="${y}" x2="${x+w}" y2="${y+h}" stroke="#e74c3c" stroke-width="${w*0.18}"/>
     <line x1="${x+w}" y1="${y}" x2="${x}" y2="${y+h}" stroke="#e74c3c" stroke-width="${w*0.18}"/>` },
  C: { name: 'Charlie', color: '#2980b9', draw: (x,y,w,h) => {
    const sh = h/5;
    return `<rect x="${x}" y="${y}" width="${w}" height="${sh}" fill="#2980b9"/>
     <rect x="${x}" y="${y+sh}" width="${w}" height="${sh}" fill="white"/>
     <rect x="${x}" y="${y+sh*2}" width="${w}" height="${sh}" fill="#e74c3c"/>
     <rect x="${x}" y="${y+sh*3}" width="${w}" height="${sh}" fill="white"/>
     <rect x="${x}" y="${y+sh*4}" width="${w}" height="${sh}" fill="#2980b9"/>`;
  }},
};

function generateFlagScene(qText) {
  const q = qText || '';
  // Detect which flags are referenced. A hoist reads top-down, so the flags are
  // ordered by where they appear in the question text, not by match order here.
  const FLAG_PATTERNS = [
    ['Q', /Quebec|'Q'|דגל\s+Q\b|תמונה 106/i],
    ['O', /Oscar|'O'|דגל\s+O\b|תמונה 104/i],
    ['A', /Alpha|'A'|דגל\s+A\b|תמונה 98/i],
    ['B', /Bravo|'B'|דגל\s+B\b|תמונה 95/i],
    ['N', /דגל N\b|תמונה 93/i],
    ['C', /דגל C\b|תמונה 92/i],
    ['V', /דגל V\b/i],
  ];
  let flags = FLAG_PATTERNS
    .map(([letter, re]) => ({ letter, at: q.search(re) }))
    .filter(m => m.at >= 0)
    .sort((a, b) => a.at - b.at)
    .map(m => m.letter);
  if(!flags.length && /נמל זר|כניסה.*נמל.*זר/i.test(q)) flags = ['Q'];
  if(!flags.length && /צוללים/i.test(q)) flags = ['A'];

  const SEA_Y = 320;
  const waveFilter = `
  <defs>
    <filter id="waveFlag" x="-10%" y="-10%" width="130%" height="130%">
      <feTurbulence type="turbulence" baseFrequency="0.015 0.04" numOctaves="3" seed="2" result="turb">
        <animate attributeName="baseFrequency" values="0.015 0.04;0.025 0.06;0.015 0.04" dur="2.5s" repeatCount="indefinite"/>
      </feTurbulence>
      <feDisplacementMap in="SourceGraphic" in2="turb" scale="10" xChannelSelector="R" yChannelSelector="G"/>
    </filter>
  </defs>`;

  const sky = `<rect width="360" height="420" fill="#050d1a"/>
  <circle cx="40" cy="22" r="1" fill="white" opacity=".5"/>
  <circle cx="110" cy="14" r="1.2" fill="white" opacity=".6"/>
  <circle cx="200" cy="28" r="1" fill="white" opacity=".4"/>
  <circle cx="290" cy="16" r="1.3" fill="white" opacity=".7"/>
  <circle cx="330" cy="42" r="1" fill="white" opacity=".5"/>`;

  const sea = `
  <rect x="0" y="${SEA_Y}" width="360" height="${420-SEA_Y}" fill="#0a1f3a"/>
  <path d="M0 ${SEA_Y+8} Q90 ${SEA_Y} 180 ${SEA_Y+8} Q270 ${SEA_Y+16} 360 ${SEA_Y+8}" fill="none" stroke="#1a4a6a" stroke-width="1.5" opacity=".5">
    <animate attributeName="d" values="M0 ${SEA_Y+8} Q90 ${SEA_Y} 180 ${SEA_Y+8} Q270 ${SEA_Y+16} 360 ${SEA_Y+8};M0 ${SEA_Y+4} Q90 ${SEA_Y+12} 180 ${SEA_Y+4} Q270 ${SEA_Y-2} 360 ${SEA_Y+4};M0 ${SEA_Y+8} Q90 ${SEA_Y} 180 ${SEA_Y+8} Q270 ${SEA_Y+16} 360 ${SEA_Y+8}" dur="4s" repeatCount="indefinite"/>
  </path>`;

  // Q#262 - stern view with Israel flag, Q starboard, host country port
  if (/נמל זר|כניסה.*נמל.*זר/i.test(q)) {
    const hullY = SEA_Y - 60;
    const hull = `
    <path d="M90,${hullY+60} Q90,${hullY+80} 130,${SEA_Y+10} L230,${SEA_Y+10} Q270,${hullY+80} 270,${hullY+60} Z" fill="#1a3a5a" stroke="#2a5a8a" stroke-width="1.5"/>
    <path d="M110,${hullY+60} L250,${hullY+60}" stroke="#2a5a8a" stroke-width="0.8" opacity=".5"/>
    <rect x="120" y="${hullY+30}" width="120" height="30" rx="3" fill="#0f2a44" stroke="#2a5a8a" stroke-width="0.8"/>
    <rect x="140" y="${hullY+35}" width="14" height="10" rx="2" fill="#1a4a6a" opacity=".7"/>
    <rect x="165" y="${hullY+35}" width="14" height="10" rx="2" fill="#1a4a6a" opacity=".7"/>
    <rect x="190" y="${hullY+35}" width="14" height="10" rx="2" fill="#1a4a6a" opacity=".7"/>
    <rect x="215" y="${hullY+35}" width="14" height="10" rx="2" fill="#1a4a6a" opacity=".7"/>`;
    const mastX = 180;
    const mastTop = 40;
    const mast = `<rect x="${mastX-2}" y="${mastTop}" width="4" height="${hullY+30-mastTop}" fill="#6B5335" stroke="#5a4530" stroke-width="0.5"/>
    <circle cx="${mastX}" cy="${mastTop-3}" r="4" fill="#8B7355" stroke="#6B5335" stroke-width="1"/>
    <rect x="${mastX-30}" y="${mastTop+20}" width="60" height="3" rx="1" fill="#6B5335"/>`;
    const fq = SIGNAL_FLAGS['Q'];
    const fw = 50, fh = 35;
    const qFlag = `<g filter="url(#waveFlag)">
      <rect x="${mastX+32}" y="${mastTop+24}" width="2" height="${fh+6}" fill="#6B5335"/>
      ${fq.draw(mastX+34, mastTop+26, fw, fh)}
    </g>
    <text x="${mastX+34+fw/2}" y="${mastTop+26+fh+14}" text-anchor="middle" fill="${fq.color}" font-size="10" font-family="Heebo,sans-serif" font-weight="700">Q - Quebec</text>
    <text x="${mastX+34+fw/2}" y="${mastTop+26+fh+26}" text-anchor="middle" fill="#aaa" font-size="9" font-family="Heebo,sans-serif">דופן ימין</text>`;
    const hostFlag = `<g filter="url(#waveFlag)">
      <rect x="${mastX-34}" y="${mastTop+24}" width="2" height="${fh+6}" fill="#6B5335"/>
      <rect x="${mastX-34-fw}" y="${mastTop+26}" width="${fw}" height="${fh}" fill="#e74c3c"/>
      <rect x="${mastX-34-fw}" y="${mastTop+26+fh/3}" width="${fw}" height="${fh/3}" fill="white"/>
    </g>
    <text x="${mastX-34-fw/2}" y="${mastTop+26+fh+14}" text-anchor="middle" fill="#e0e0e0" font-size="10" font-family="Heebo,sans-serif" font-weight="700">דגל מארח</text>
    <text x="${mastX-34-fw/2}" y="${mastTop+26+fh+26}" text-anchor="middle" fill="#aaa" font-size="9" font-family="Heebo,sans-serif">דופן שמאל</text>`;
    const sternPoleX = 255;
    const sternPoleTop = hullY + 5;
    const isw = 44, ish = 30;
    const cx = sternPoleX+4+isw/2, cy = sternPoleTop+2+ish/2;
    const r = ish*0.28;
    const israelFlag = `
    <rect x="${sternPoleX}" y="${sternPoleTop}" width="3" height="${hullY+55-sternPoleTop}" rx="1" fill="#8B7355"/>
    <g filter="url(#waveFlag)">
      <rect x="${sternPoleX+4}" y="${sternPoleTop+2}" width="${isw}" height="${ish}" fill="white"/>
      <rect x="${sternPoleX+4}" y="${sternPoleTop+2}" width="${isw}" height="${ish*0.22}" fill="#2980b9"/>
      <rect x="${sternPoleX+4}" y="${sternPoleTop+2+ish*0.78}" width="${isw}" height="${ish*0.22}" fill="#2980b9"/>
      <polygon points="${cx},${cy-r} ${cx+r*0.866},${cy+r*0.5} ${cx-r*0.866},${cy+r*0.5}" fill="none" stroke="#2980b9" stroke-width="1.2"/>
      <polygon points="${cx},${cy+r} ${cx+r*0.866},${cy-r*0.5} ${cx-r*0.866},${cy-r*0.5}" fill="none" stroke="#2980b9" stroke-width="1.2"/>
    </g>
    <text x="${sternPoleX+4+isw/2}" y="${sternPoleTop+ish+18}" text-anchor="middle" fill="#7eb8f7" font-size="9" font-family="Heebo,sans-serif" font-weight="700">דגל ישראל</text>
    <text x="${sternPoleX+4+isw/2}" y="${sternPoleTop+ish+29}" text-anchor="middle" fill="#aaa" font-size="9" font-family="Heebo,sans-serif">ירכתיים</text>`;
    return `${waveFilter}${sky}${sea}${hull}${mast}${qFlag}${hostFlag}${israelFlag}`;
  }

  let flagsSvg = '';
  if (flags.length === 0) {
    // No flag identified: draw no flag rather than guessing one.
    flagsSvg = '';
  } else if (flags.length === 1) {
    // Single large flag
    const f = SIGNAL_FLAGS[flags[0]];
    const FW = 140, FH = 100, FX = 120, FY = 80;
    const poleX = FX - 4;
    // Pole
    flagsSvg += `<rect x="${poleX}" y="${FY-20}" width="6" height="${SEA_Y-FY+20}" rx="2" fill="#8B7355" stroke="#6B5335" stroke-width="1"/>`;
    // Flag with wave filter
    flagsSvg += `<g filter="url(#waveFlag)">${f.draw(FX, FY, FW, FH)}</g>`;
    // Rope ties
    flagsSvg += `<circle cx="${poleX+3}" cy="${FY}" r="2.5" fill="#6B5335"/>`;
    flagsSvg += `<circle cx="${poleX+3}" cy="${FY+FH}" r="2.5" fill="#6B5335"/>`;
    // Label
    flagsSvg += `<text x="${FX+FW/2}" y="${FY+FH+24}" text-anchor="middle" fill="${f.color}" font-size="14" font-family="Heebo,sans-serif" font-weight="900">${flags[0]} - ${f.name}</text>`;
    flagsSvg += `<text x="${FX+FW/2}" y="${FY+FH+40}" text-anchor="middle" fill="#7eb8f7" font-size="10" font-family="Heebo,sans-serif" opacity=".8">International Signal Flag</text>`;
  } else {
    // Multiple flags on same pole (like N over V for distress)
    const FW = 100, FH = 70, FX = 130, gap = 12;
    const startY = 60;
    const poleX = FX - 4;
    const totalH = flags.length * FH + (flags.length-1) * gap;
    flagsSvg += `<rect x="${poleX}" y="${startY-20}" width="6" height="${SEA_Y-startY+20}" rx="2" fill="#8B7355" stroke="#6B5335" stroke-width="1"/>`;
    flags.forEach((key, i) => {
      const f = SIGNAL_FLAGS[key];
      const fy = startY + i * (FH + gap);
      flagsSvg += `<g filter="url(#waveFlag)">${f.draw(FX, fy, FW, FH)}</g>`;
      flagsSvg += `<circle cx="${poleX+3}" cy="${fy}" r="2.5" fill="#6B5335"/>`;
      flagsSvg += `<circle cx="${poleX+3}" cy="${fy+FH}" r="2.5" fill="#6B5335"/>`;
      flagsSvg += `<text x="${FX+FW+10}" y="${fy+FH/2+4}" fill="${f.color}" font-size="12" font-family="Heebo,sans-serif" font-weight="700">${key} - ${f.name}</text>`;
    });
  }

  // Boat silhouette at waterline
  const boat = `
  <path d="M100,${SEA_Y} L260,${SEA_Y} L248,${SEA_Y+14} L112,${SEA_Y+14} Z" fill="#1a3a5a" stroke="#2a5a8a" stroke-width="1"/>
  <rect x="160" y="${SEA_Y-30}" width="4" height="30" fill="#2a5a8a"/>
  <rect x="200" y="${SEA_Y-20}" width="3" height="20" fill="#2a5a8a"/>`;

  return `${waveFilter}${sky}${sea}${boat}${flagsSvg}`;
}

function generateSoundSignalScene(pattern, qText, answerText) {
  const SHORT_R = 10, LONG_W = 56, LONG_H = 18, GAP = 14, CY = 158;
  const SIG_COLOR = '#e74c3c';
  const ctx = (qText || '') + ' ' + (answerText || '');
  const isOvertake  = /עוקפת|עוקף|overtake/i.test(ctx);
  const isSailboat  = /מפרש|sailboat|sailing vessel/i.test(ctx);
  const isBell      = /פעמון|bell|גונג/i.test(ctx) || /עוגנ/i.test(ctx);

  // ── Blast timing ──────────────────────────────────────────────────────────
  const starts = [];
  let t = 0.4;
  pattern.forEach(b => { starts.push(t); t += BLAST_DUR[b] + BLAST_GAP; });

  // ── Blast symbols (only for horn-signal questions, not bell) ─────────────
  const MAX_W = 340;
  const totalW = pattern.reduce((s,b) => s + (b==='L' ? LONG_W : SHORT_R*2), 0) + GAP*(pattern.length-1);
  const scale = totalW > MAX_W ? MAX_W / totalW : 1;
  let x = 180 - totalW / 2;
  let blastEls = '';
  if (!isBell) {
    pattern.forEach((b, i) => {
      const bs = starts[i].toFixed(2) + 's';
      const anim = `<animate attributeName="opacity" from="0" to="1" begin="${bs}" dur="0.05s" fill="freeze"/>`;
      if (b === 'L') {
        blastEls += `<rect x="${x.toFixed(1)}" y="${(CY-LONG_H/2).toFixed(1)}" width="${LONG_W}" height="${LONG_H}" rx="3" fill="${SIG_COLOR}" opacity="0">${anim}</rect>`;
        blastEls += `<text x="${(x+LONG_W/2).toFixed(1)}" y="${(CY+LONG_H/2+13).toFixed(1)}" text-anchor="middle" fill="${SIG_COLOR}" font-size="9" font-family="Heebo,sans-serif" opacity="0">ארוכה${anim}</text>`;
        x += LONG_W + GAP;
      } else {
        const bcx = x + SHORT_R;
        blastEls += `<circle cx="${bcx.toFixed(1)}" cy="${CY}" r="${SHORT_R}" fill="${SIG_COLOR}" opacity="0">${anim}</circle>`;
        blastEls += `<text x="${bcx.toFixed(1)}" y="${(CY+SHORT_R+13).toFixed(1)}" text-anchor="middle" fill="${SIG_COLOR}" font-size="9" font-family="Heebo,sans-serif" opacity="0">קצרה${anim}</text>`;
        x += SHORT_R*2 + GAP;
      }
    });
    if (scale < 1) {
      blastEls = `<g transform="translate(180,${CY}) scale(${scale.toFixed(3)}) translate(-180,-${CY})">${blastEls}</g>`;
    }
  }

  // ── Boat scene ────────────────────────────────────────────────────────────
  const SEA_Y = 310;
  const seaBg = `
  <rect x="0" y="${SEA_Y}" width="360" height="${420-SEA_Y}" fill="#0a1f3a"/>
  <path d="M0 ${SEA_Y+5} Q90 ${SEA_Y-3} 180 ${SEA_Y+5} Q270 ${SEA_Y+13} 360 ${SEA_Y+5}" fill="none" stroke="#1a4a6a" stroke-width="1.5" opacity=".6"/>
  <path d="M0 ${SEA_Y+18} Q60 ${SEA_Y+10} 120 ${SEA_Y+18} Q180 ${SEA_Y+26} 240 ${SEA_Y+18} Q300 ${SEA_Y+10} 360 ${SEA_Y+18}" fill="none" stroke="#1a4a6a" stroke-width="1" opacity=".35"/>`;

  let boatScene;
  if (isOvertake) {
    // Two boats — top-down view
    boatScene = seaBg + `
  <rect x="0" y="${SEA_Y}" width="360" height="58" fill="#0d2440" opacity=".6"/>
  <line x1="0" y1="${SEA_Y}" x2="360" y2="${SEA_Y}" stroke="#1e4a6e" stroke-width="1" stroke-dasharray="8,5"/>
  <line x1="0" y1="${SEA_Y+58}" x2="360" y2="${SEA_Y+58}" stroke="#1e4a6e" stroke-width="1" stroke-dasharray="8,5"/>
  ${topBoat(95, SEA_Y+20, '#f1c40f', '#c8a000', 'עוקפת')}
  ${topBoat(230, SEA_Y+38, '#1abc9c', '#148f77', 'נעקפת')}
  <text x="180" y="408" text-anchor="middle" fill="#7eb8f7" font-size="8" font-family="Heebo,sans-serif" opacity=".7">נתיב צר — מבט מלמעלה</text>`;
  } else if (isSailboat) {
    // Sailboat scene — large purple sailboat side view
    boatScene = seaBg + `
  <!-- Sailboat hull -->
  <path d="M${100},${SEA_Y} L${260},${SEA_Y} L${248},${SEA_Y+16} L${112},${SEA_Y+16} Z"
        fill="#8e44ad" stroke="#6c3483" stroke-width="1.5"/>
  <!-- Boom -->
  <line x1="${115}" y1="${SEA_Y-4}" x2="${255}" y2="${SEA_Y-4}" stroke="#6c3483" stroke-width="3"/>
  <!-- Mast -->
  <line x1="${180}" y1="${SEA_Y-4}" x2="${180}" y2="${SEA_Y-145}" stroke="#6c3483" stroke-width="2.5"/>
  <!-- Main sail -->
  <path d="M${180},${SEA_Y-145} L${180},${SEA_Y-4} L${255},${SEA_Y-4} Z"
        fill="#9b59b6" opacity=".85" stroke="#7d3c98" stroke-width="1"/>
  <!-- Jib (foresail) -->
  <path d="M${180},${SEA_Y-110} L${180},${SEA_Y-4} L${110},${SEA_Y-4} Z"
        fill="#7d3c98" opacity=".8" stroke="#6c3483" stroke-width="1"/>
  <!-- Forestay -->
  <line x1="${180}" y1="${SEA_Y-145}" x2="${108}" y2="${SEA_Y-4}" stroke="#6c3483" stroke-width="1" opacity=".6"/>
  <!-- Shrouds -->
  <line x1="${180}" y1="${SEA_Y-100}" x2="${120}" y2="${SEA_Y-4}" stroke="#6c3483" stroke-width="0.8" opacity=".5"/>
  <line x1="${180}" y1="${SEA_Y-100}" x2="${240}" y2="${SEA_Y-4}" stroke="#6c3483" stroke-width="0.8" opacity=".5"/>
  <text x="180" y="408" text-anchor="middle" fill="#9b59b6" font-size="9" font-family="Heebo,sans-serif" font-weight="700" opacity=".8">מפרשית — Sailing Vessel</text>`;
  } else if (isBell) {
    // Anchored vessel: anchor light (white 360°) + bell visual
    const bx = 175;
    const mastX = bx - 30, mastTopY = SEA_Y - 86;
    boatScene = seaBg + sideBoat(bx, SEA_Y, '#f1c40f', '#c8a000') + `
  <!-- Anchor chain -->
  <line x1="${bx+10}" y1="${SEA_Y+14}" x2="${bx+10}" y2="${SEA_Y+40}" stroke="#7eb8f7" stroke-width="1.5" stroke-dasharray="3,3" opacity=".6"/>
  <text x="${bx+10}" y="${SEA_Y+56}" text-anchor="middle" fill="#7eb8f7" font-size="16" opacity=".7">⚓</text>
  <!-- Anchor light: white 360° on mast -->
  <circle cx="${mastX}" cy="${mastTopY}" r="22" fill="white" opacity=".08"/>
  <circle cx="${mastX}" cy="${mastTopY}" r="13" fill="white" opacity=".18"/>
  <circle cx="${mastX}" cy="${mastTopY}" r="5"  fill="white" opacity=".95"/>
  <line x1="${mastX-22}" y1="${mastTopY}" x2="${mastX+22}" y2="${mastTopY}" stroke="white" stroke-width="0.6" opacity=".25"/>
  <line x1="${mastX}" y1="${mastTopY-22}" x2="${mastX}" y2="${mastTopY+22}" stroke="white" stroke-width="0.6" opacity=".25"/>
  <text x="${mastX}" y="${mastTopY-26}" text-anchor="middle" fill="white" font-size="7" font-family="Heebo,sans-serif" font-weight="700" opacity=".8">360° לבן</text>
  <!-- Bell (upper-right of scene) -->
  <g transform="translate(272,168)">
    <path d="M-26,28 Q-32,-4 -32,-28 Q-32,-56 0,-60 Q32,-56 32,-28 Q32,-4 26,28 Z" fill="#f1c40f" stroke="#c8a000" stroke-width="2"/>
    <path d="M-30,28 Q0,44 30,28" fill="none" stroke="#c8a000" stroke-width="3"/>
    <line x1="0" y1="28" x2="0" y2="48" stroke="#c8a000" stroke-width="3"/>
    <circle cx="0" cy="52" r="7" fill="#c8a000"/>
    <path d="M-5,-60 Q0,-72 5,-60" fill="none" stroke="#c8a000" stroke-width="2.5"/>
    <path d="M38,-18 Q50,-8 38,8" fill="none" stroke="white" stroke-width="1.5" opacity=".55"/>
    <path d="M48,-22 Q64,-8 48,12" fill="none" stroke="white" stroke-width="1" opacity=".3"/>
    <path d="M-38,-18 Q-50,-8 -38,8" fill="none" stroke="white" stroke-width="1.5" opacity=".55"/>
    <path d="M-48,-22 Q-64,-8 -48,12" fill="none" stroke="white" stroke-width="1" opacity=".3"/>
  </g>
  <text x="272" y="232" text-anchor="middle" fill="#f1c40f" font-size="9" font-family="Heebo,sans-serif" font-weight="700">5 שניות / כל דקה</text>`;
  } else {
    // Single yellow motorboat — side view
    boatScene = seaBg + sideBoat(175, SEA_Y, '#f1c40f', '#c8a000');
  }

  return `
  <rect width="360" height="420" fill="#050d1a"/>
  <circle cx="40" cy="22" r="1" fill="white" opacity=".5"/>
  <circle cx="110" cy="14" r="1.2" fill="white" opacity=".6"/>
  <circle cx="200" cy="28" r="1" fill="white" opacity=".4"/>
  <circle cx="290" cy="16" r="1.3" fill="white" opacity=".7"/>
  ${boatScene}
  ${blastEls}`;
}

function generateQuizHTML(q, lang, autoPlay=false) {
  lang = lang || currentLang || 'he';
  const isEn = lang === 'en';
  const LT = isEn ? LETTERS_EN : LETTERS_HE;
  const qText = isEn ? (q.q_en || q.q_he || '') : (q.q_he || q.q_en || '');
  const opts = q.options || [];
  const correctI = letterToIdx(q.answer);
  const expl = q.explanation || '';
  const correctText = (opts[correctI]||'').replace(/^[אבגדABCDabcd]\.\s*/,'');
  const isSoundSignal = q.topic === 'אותות קוליים';
  const blastPattern = isSoundSignal ? parseBlastPatternMulti(correctText, qText, expl, q.blastOverride||'') : null;
  const hasVesselLetters = /\([A-P]\)/.test(qText) || /(?:כלי.(?:ה)?שייט|אופנוע.ים|מפרשית)\s+[A-P]\b/.test(qText);
  const scene = (isSoundSignal && !hasVesselLetters)
    ? generateSoundSignalScene(blastPattern, qText, correctText)
    : getScene(q.topic, q.q_he||q.q_en);
  const optsHtml = opts.slice(0,4).map((o,i)=>{
    const t = o.replace(/^[אבגדABCDabcd]\.\s*/,'');
    return `<div class="opt" id="o${i}"><div class="ltr">${LT[i]}</div>${t}</div>`;
  }).join('');
  const headerTitle = isEn ? "Alex Argov's Daily Skipper Quiz" : 'מבחן הסקיפר היומי של אלכס ארגוב';
  const dir = isEn ? 'ltr' : 'rtl';
  const lang_he = isEn ? 'en' : 'he';
  // Media scene
  const sceneContent = q.mediaUrl
    ? (q.mediaType === 'video'
        ? `<video src="${q.mediaUrl}" autoplay muted loop playsinline style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:1"></video>`
        : `<img src="${q.mediaUrl}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:1">`)
    : '';
  const svgZindex = q.mediaUrl ? 'position:absolute;inset:0;z-index:2;' : '';

  const followText = isEn ? '⚓ Follow Daily Skipper Quiz' : '⚓ עקבו למבחן הסקיפר היומי';
  const correctLabel = isEn ? 'Correct Answer!' : 'תשובה נכונה!';
  const phaseLabels = isEn
    ? ['❓ Question','💭 Think...','✅ Correct Answer','💡 Explanation']
    : ['❓ השאלה','💭 חשוב על התשובה...','✅ התשובה הנכונה','💡 הסבר'];

  return `<!DOCTYPE html>
<html dir="${dir}" lang="${lang_he}"><head><meta charset="UTF-8">
<title>Skipper Quiz #${q.num} — ${q.topic||''}</title>
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;700;900&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000;display:flex;align-items:center;justify-content:center;height:100vh;overflow:hidden}
#reel{width:390px;height:625px;background:#0c1a3a;overflow:hidden;position:relative;display:flex;flex-direction:column;font-family:'Heebo',sans-serif;direction:${dir}}
#hdr{background:#0c1a3a;padding:14px 16px 10px;flex-shrink:0;border-bottom:2px solid #1e3a6e;text-align:center}
.brand{color:#7eb8f7;font-size:11px;font-weight:700;letter-spacing:2px;margin-bottom:2px}
.htitle{color:#fff;font-size:18px;font-weight:900}
#scene{flex:1;position:relative;overflow:hidden}
#ftr{background:#0c1a3a;padding:12px 16px;flex-shrink:0;border-top:2px solid #1e3a6e}
.ql{color:#7eb8f7;font-size:11px;font-weight:700;letter-spacing:1px;margin-bottom:5px}
.qt{color:#fff;font-size:13px;font-weight:700;line-height:1.4;margin-bottom:8px}
.opts{display:flex;flex-direction:column;gap:5px}
.opt{background:#1a2f5e;border:1px solid #2a4a8a;border-radius:7px;padding:7px 10px;color:#fff;font-size:12px;font-weight:700;display:flex;align-items:center;gap:8px;transition:all 0.5s}
.ltr{background:#0c1a3a;color:#7eb8f7;font-size:11px;min-width:22px;height:22px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;font-weight:900}
.opt.correct{background:#0d3d2a;border-color:#2ecc71;color:#2ecc71}
.opt.correct .ltr{background:#2ecc71;color:#0d3d2a}
.opt.wrong{background:#3d1a1a;border-color:#e74c3c;color:#e74c3c}
.opt.wrong .ltr{background:#e74c3c;color:#fff}
.opt.dim{opacity:0.3}
#prog{position:absolute;bottom:0;left:0;height:2px;background:#4a90d9;width:0;z-index:5}
</style></head><body>
<div id="reel">
  <div id="hdr"><div class="brand">⚓ SKIPPER QUIZ</div><div class="htitle">${headerTitle}</div></div>
  <div id="scene">
    ${sceneContent}
    <svg width="100%" height="100%" viewBox="0 0 360 420" preserveAspectRatio="xMidYMid slice" style="${svgZindex}">
      ${q.mediaUrl ? '' : scene}
      <g id="ov" opacity="0">
        <rect x="60" y="8" width="240" height="38" rx="19" fill="#0d3d2a" stroke="#2ecc71" stroke-width="2" opacity="0.95"/>
        <text id="ovText" x="180" y="32" text-anchor="middle" fill="#2ecc71" font-size="20" font-family="Heebo,sans-serif" font-weight="900">✅ נכון!</text>
      </g>
      ${q.topic !== 'אותות קוליים' ? '<text x="180" y="345" text-anchor="middle" fill="#7eb8f7" font-size="12" font-family="Heebo,sans-serif" font-weight="700" opacity="1">⚓ Alex Argov | Sailing Instructor</text>' : ''}
    </svg>
    <div id="prog"></div>
  </div>
  <div id="ftr">
    <div class="ql" id="ql">${phaseLabels[0]}</div>
    <div class="qt" id="qt">${qText}</div>
    <div class="opts" id="opts">${optsHtml}</div>
  </div>
</div>
<script>
const C=${correctI};
const OPTS=${JSON.stringify(opts)};
const Q=${JSON.stringify(qText)};
const E=${JSON.stringify(expl)};
const LT=${JSON.stringify(isEn ? LETTERS_EN : LETTERS_HE)};
${autoPlay ? `
// AUTO-PLAY MODE — countdown then reveal (for screen recording)
// Gated behind window.__startAutoPlay() instead of running on page load, so the
// recorder (Puppeteer) can fire it the instant the screencast actually starts —
// otherwise the timer head-starts before recording begins and drifts out of sync
// with the audio track (which assumes recording-start == t=0).
window.__startAutoPlay = function(){
const prog=document.getElementById('prog');
const DELAY=15000;
prog.style.transition='none';prog.style.width='0%';
setTimeout(()=>{prog.style.transition='width '+DELAY+'ms linear';prog.style.width='100%';},30);
setTimeout(()=>{
  document.querySelectorAll('.opt').forEach((o,j)=>{
    o.style.transition='all 0.6s';
    if(j===C)o.classList.add('correct'); else o.classList.add('dim');
  });
  const ov=document.getElementById('ov');
  const txt=document.getElementById('ovText');
  const rect=ov.querySelector('rect');
  txt.textContent='✅ תשובה נכונה!';txt.setAttribute('fill','#2ecc71');
  rect.setAttribute('fill','#0d3d2a');rect.setAttribute('stroke','#2ecc71');
  ov.setAttribute('opacity','1');
  setTimeout(()=>{
    document.getElementById('ql').textContent='✅ התשובה הנכונה:';
    document.getElementById('qt').innerHTML='<span style="color:#2ecc71;font-size:11px;font-weight:900">'+OPTS[C]+'</span>'+(E?'<br><span style="color:#aac4e8;font-size:10px;font-weight:400">'+E+'</span>':'');
    // Second countdown — next card (loop for batch recording)
    const prog2=document.getElementById('prog');
    prog2.style.transition='none';prog2.style.width='0%';
    setTimeout(()=>{prog2.style.transition='width 4000ms linear';prog2.style.width='100%';},30);
  },600);
},DELAY+50);
};
` : `
let answered=false;
document.querySelectorAll('.opt').forEach((el,i)=>{
  el.style.cursor='pointer';
  el.addEventListener('click',()=>{
    if(answered)return;
    answered=true;
    const ok=(i===C);
    document.querySelectorAll('.opt').forEach((o,j)=>{
      o.style.cursor='default';
      if(j===C)o.classList.add('correct');
      else if(j===i&&!ok)o.classList.add('wrong');
      else o.classList.add('dim');
    });
    const ov=document.getElementById('ov');
    const txt=document.getElementById('ovText');
    const rect=ov.querySelector('rect');
    if(ok){txt.textContent='✅ נכון!';txt.setAttribute('fill','#2ecc71');rect.setAttribute('fill','#0d3d2a');rect.setAttribute('stroke','#2ecc71');}
    else{txt.textContent='❌ לא נכון';txt.setAttribute('fill','#e74c3c');rect.setAttribute('fill','#3d1a1a');rect.setAttribute('stroke','#e74c3c');}
    ov.setAttribute('opacity','1');
    setTimeout(()=>{
      document.getElementById('ql').textContent=ok?'✅ נכון! הסבר:':'❌ תשובה נכונה: '+LT[C];
      document.getElementById('qt').innerHTML='<span style="color:'+(ok?'#2ecc71':'#e67e22')+';font-size:11px;font-weight:900">'+(OPTS[C]||'')+'</span>'+(E?'<br><span style="color:#aac4e8;font-size:10px;font-weight:400">'+E+'</span>':'');
    },ok?500:800);
  });
});
`}
${isSoundSignal ? `
// ── Sound signal audio ──────────────────────────────────────────────────────
const _BP=${JSON.stringify(blastPattern)};
const _BD={L:${BLAST_DUR.L},S:${BLAST_DUR.S}},_BG=${BLAST_GAP};
let _played=false;
function _playBlasts(){
  if(_played)return;_played=true;
  try{
    const ctx=new(window.AudioContext||window.webkitAudioContext)();
    let t=ctx.currentTime+0.4;
    _BP.forEach(b=>{
      const dur=_BD[b];
      [[150,0.50],[300,0.22],[450,0.10],[600,0.05]].forEach(([f,a])=>{
        const o=ctx.createOscillator(),g=ctx.createGain();
        o.type='sawtooth';o.frequency.value=f;
        g.gain.setValueAtTime(0.001,t);
        g.gain.linearRampToValueAtTime(a,t+0.04);
        g.gain.setValueAtTime(a,t+dur-0.07);
        g.gain.linearRampToValueAtTime(0.001,t+dur);
        o.connect(g);g.connect(ctx.destination);
        o.start(t);o.stop(t+dur+0.05);
      });
      t+=dur+_BG;
    });
  }catch(e){_played=false;}
}
// Autoplay on load; retry on first click if browser blocks
window.addEventListener('load',()=>setTimeout(_playBlasts,350));
document.addEventListener('click',()=>{_played=false;_playBlasts();},{once:true});
` : ''}
<\/script></body></html>`;
}
