"""Recorrido didáctico del Transformer con los tokens de una traducción real."""

import json


def crear_diagrama(texto, resultado):
    # Evita que el texto del usuario pueda cerrar el script del diagrama.
    datos = json.dumps({"texto": texto, **resultado}, ensure_ascii=True).replace("<", "\\u003c")
    return HTML.replace("__DATOS__", datos)


HTML = r'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* { box-sizing: border-box }
html { color-scheme: dark }
body { margin: 0; color: #e7edf8; font: 14px system-ui, sans-serif; background: #101827 }
main { max-width: 1440px; margin: auto; padding: 20px; border: 1px solid #314259; border-radius: 16px;
       background: radial-gradient(ellipse at top left, #192d43, #101827 65%) }
header { display: flex; justify-content: space-between; align-items: center; gap: 12px }
h2 { font-size: 19px; margin: 4px 0 }
.eyebrow { color: #6ee7ce; font-size: 11px; letter-spacing: 2px }
.muted { color: #acbad0; font-size: 12px; line-height: 1.5 }
#counter { white-space: nowrap; color: #6ee7ce; font-size: 12px }
.track { height: 3px; background: #2c3c52; margin: 16px 0 4px; border-radius: 3px }
#progress { height: 100%; background: #6ee7ce; transition: width .35s }
.canvas { overflow-x: auto }
svg { display: block; width: 100%; height: auto }
.node rect { fill: #182538; stroke: #3b4d67; stroke-width: 1.2; transition: all .3s }
.node text { fill: #edf4ff; font-size: 13px; text-anchor: middle }
.node .small { fill: #a6b7ce; font-size: 10px }
.node.active rect { fill: #153e44; stroke: #6ee7ce; stroke-width: 2;
                    filter: drop-shadow(0 0 5px #6ee7ce44) }
.node.done rect { stroke: #43847e }
.edge { fill: none; stroke: #536983; stroke-width: 1.7; marker-end: url(#arrow) }
.edge.active { stroke: #6ee7ce; stroke-width: 2.5; stroke-dasharray: 7 5; animation: flow .7s linear infinite }
.label { fill: #a6b7ce; font-size: 10px }
@keyframes flow { to { stroke-dashoffset: -24 } }
.detail { border: 1px solid #34465f; background: #152235; border-radius: 12px; padding: 14px; min-height: 200px }
.detail h3 { font-size: 16px; margin: 0 0 7px; color: #6ee7ce }
.detail p { font-size: 13px; margin: 0 0 10px; line-height: 1.5 }
#data { max-height: 190px; overflow: auto; overflow-wrap: anywhere; white-space: pre-wrap; font-size: 12px; color: #d5e2f5 }
nav { display: flex; justify-content: space-between; align-items: center; gap: 10px; margin-top: 14px }
button { background: #20344a; color: #ecf5ff; border: 1px solid #58728d; border-radius: 8px;
         padding: 10px 14px; font: inherit; cursor: pointer }
button:hover:enabled { background: #2b4c5e; border-color: #6ee7ce }
button:disabled { opacity: .35; cursor: default }
button:focus-visible { outline: 3px solid #6ee7ce; outline-offset: 3px }
.note { margin: 12px 0 0 }
.group { fill: #111f32; stroke: #597089; stroke-width: 1.5 }
.group-label { fill: #a9c7ec; font-size: 14px; font-weight: 600 }
.formula { color: #9dc5ff; font-family: ui-monospace, monospace; margin: 10px 0; overflow-wrap: anywhere }
.sample { margin: 12px 0 8px; color: #e7edf8; font-size: 13px }
table { width: 100%; border-collapse: collapse; white-space: normal; text-align: left }
th { color: #99adc6; font-size: 11px; font-weight: 500 }
td, th { padding: 7px 5px; border-bottom: 1px solid #30455c; overflow-wrap: anywhere }
td:last-child { color: #6ee7ce }
#representation { color: #acbad0; font-size: 11px; margin: 8px 0 }

.workspace { display: grid; grid-template-columns: minmax(0, 2fr) minmax(0, 3fr); gap: 24px; margin-top: 20px; align-items: start }
.map { position: sticky; top: 12px; min-width: 0 }
.detail { min-width: 0; padding: 20px }
.scene-toolbar { display: flex; align-items: center; flex-wrap: wrap; gap: 8px; margin: 12px 0 }
.scene-toolbar button, select { padding: 8px 12px; font: inherit; border-radius: 8px; color: #edf4ff; background: #20344a; border: 1px solid #58728d }
.scene-toolbar label { margin-left: auto; font-size: 12px; color: #acbad0 }
select:focus-visible, summary:focus-visible { outline: 3px solid #6ee7ce; outline-offset: 3px }
.scene-viewport { overflow-x: auto }
#scene { background: radial-gradient(ellipse at top, #20374b, #111d2e 80%); border: 1px solid #34465f; border-radius: 12px }
#scene text { font-family: system-ui, sans-serif; fill: #edf4ff; font-size: 18px }
#scene .scene-label { fill: #a8bed6; font-size: 15px; letter-spacing: 1px }
#scene .scene-small { fill: #bdcce0; font-size: 15px }
#scene .scene-line { fill: none; stroke: #7dddc8; stroke-width: 2; marker-end: url(#arrow) }
#scene-note { min-height: 40px; margin-top: 10px; color: #bdcce0 }
#motion-status { color: #6ee7ce; font-size: 12px }
details { border-top: 1px solid #34465f; padding-top: 12px; margin-top: 12px }
summary { cursor: pointer; color: #a9c7ec; padding: 4px 0 12px }
@media (max-width: 980px) { .workspace { grid-template-columns: 1fr } .map { position: static } .canvas { max-width: 620px; margin: auto } }
@media (max-width: 450px) { main { padding: 12px } .detail { padding: 12px } h2 { font-size: 16px } nav .muted { display: none } .canvas > svg { min-width: 490px } #scene text { font-size: 22px } #scene .scene-small { font-size: 19px } #scene .scene-label { font-size: 18px } .scene-toolbar label { margin-left: 0 } }
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation: none !important; transition: none !important } }
</style>
</head>
<body>
<main>
<header><div><div class="eyebrow">DENTRO DEL TRANSFORMER</div><h2>De un idioma a otro</h2></div><span id="counter"></span></header>
<p class="sample">Seguimos: <strong id="sample"></strong></p>
<div class="track"><div id="progress"></div></div>
<div class="workspace"><div class="map"><div class="canvas">
<svg viewBox="0 0 660 680" role="img" aria-label="Arquitectura encoder-decoder: entrada, tokens, embeddings, encoder, contexto, decoder, probabilidades, beam search y traducción">
<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#81a3b5"/></marker></defs>
<text x="30" y="20" class="label">ENTRADA · ENCODER</text><text x="375" y="20" class="label">GENERACIÓN · DECODER</text>
<rect class="group" x="30" y="244" width="240" height="275" rx="12"/>
<text x="45" y="265" class="group-label" id="encoder-label"></text>
<rect class="group" x="375" y="174" width="240" height="368" rx="12"/>
<text x="390" y="195" class="group-label" id="decoder-label"></text>
<path class="edge" data-step="1" d="M150 69 V84"/>
<path class="edge" data-step="2" d="M150 122 V137"/>
<path class="edge" data-step="3" d="M150 175 V190"/>
<path class="edge" data-step="4" d="M150 228 V244 M150 270 V276"/>
<path class="edge" data-step="5" d="M150 314 V331"/>
<path class="edge" data-step="6" d="M150 369 V386"/>
<path class="edge" data-step="7" d="M150 424 V441"/>
<path class="edge" data-step="8" d="M150 479 V487 M150 510 V541"/>
<path class="edge" data-step="13" d="M270 560 H323 V335 H390"/>
<text x="318" y="510" class="label" transform="rotate(-90 318 510)">K, V del encoder → cross-attention</text>
<path class="edge" data-step="10" d="M495 69 V91"/>
<path class="edge" data-step="11" d="M495 139 V174 M495 200 V206"/>
<path class="edge" data-step="12" d="M495 244 V260"/>
<path class="edge" data-step="13" d="M495 298 V316"/>
<path class="edge" data-step="14" d="M495 354 V370"/>
<path class="edge" data-step="15" d="M495 408 V426"/>
<path class="edge" data-step="16" d="M495 464 V480"/>
<path class="edge" data-step="17" d="M495 518 V523 M495 543 V557"/>
<path class="edge" data-step="18" d="M495 590 V605"/>
<path class="edge" data-step="19" d="M495 634 V649"/>
<path class="edge" data-step="18" d="M615 620 H643 V49 H615"/>
<g id="nodes"></g>
<text x="45" y="503" class="label">Misma estructura en cada capa</text>
<text x="390" y="534" class="label">Misma estructura en cada capa</text>
</svg>
</div>
<nav aria-label="Recorrer el proceso"><button id="prev" aria-label="Paso anterior">← Anterior</button><span id="stage" class="muted"></span><button id="next" aria-label="Paso siguiente">Siguiente →</button></nav>
</div>
<section class="detail">
<div aria-live="polite" aria-atomic="true"><h3 id="title"></h3><p id="description"></p><div id="representation"></div></div>
<div class="scene-toolbar" aria-label="Controles de animación">
<button id="play" aria-label="Pausar animación">Pausar</button><button id="replay">↻ Repetir</button>
<label for="speed">Velocidad</label><select id="speed"><option value="0.5">0,5×</option><option value="1" selected>1×</option><option value="2">2×</option></select>
</div>
<div class="scene-viewport"><svg id="scene" viewBox="0 0 620 570" role="img" aria-labelledby="scene-title scene-desc"></svg></div>
<p id="scene-note" class="muted"></p><span id="motion-status" role="status"></span>
<details><summary>Ver fórmula y datos del paso</summary><div id="formula" class="formula"></div><div id="data" tabindex="0" aria-label="Transformación de la muestra"></div></details>
</section></div>
<p class="muted note">Texto, IDs y tokens reales. Vectores y operaciones simbólicos: e, x, h… nombran representaciones, no valores medidos. La muestra de dos palabras se tokeniza por separado para explicarla; el modelo traduce la entrada completa. El decoder no traduce palabra por palabra.</p>
</main>
<script>
const d = __DATOS__;
// Cada paso resalta una operación dentro de su bloque y transforma la muestra.
const steps = [
  ['Texto de entrada', 'Observamos solo las dos primeras palabras. La traducción conserva todo el texto introducido.', '', 'Texto real', 'text', 30, 34, 240, 35, 'Texto original'],
  ['Tokenización', 'SentencePiece divide las palabras en subpalabras. Una palabra puede producir varios tokens.', 'palabras → subpalabras → IDs', 'Tokens e IDs reales de la muestra', 'tokens', 30, 84, 240, 38, 'Tokenizador'],
  ['Embedding de entrada', 'Cada ID consulta una fila de la matriz de embeddings aprendida. El vector tiene una componente por dimensión del modelo.', 'IDᵢ → E[IDᵢ] × escala', 'Vectores simbólicos', 'embedding', 30, 137, 240, 38, 'Embeddings'],
  ['Información de posición', 'Se suma la codificación posicional al embedding. Así se distingue el lugar que ocupa cada token.', 'xᵢ = eᵢ + pᵢ', 'Vectores simbólicos', 'position', 30, 190, 240, 38, 'Sumar posición'],
  ['Encoder · autoatención', `Cada token forma Q, K y V. Las ${d.cabezas} cabezas combinan información de todos los tokens de entrada, no solo de la muestra.`, 'Q = XWq, K = XWk, V = XWv; A = softmax(QKᵀ / √dk)V', 'Vectores simbólicos · atención bidireccional', 'enc-attn', 45, 276, 210, 38, 'Multi-head self-attention'],
  ['Encoder · residual y normalización', 'Se suma la entrada del subbloque a la salida de atención y se normalizan las dimensiones de cada token.', 'hᵢ = LayerNorm(xᵢ + aᵢ)', 'Vectores simbólicos', 'enc-norm', 45, 331, 210, 38, 'Suma residual + LayerNorm'],
  ['Encoder · feed-forward', 'La misma red transforma cada vector por separado: expande sus dimensiones, aplica una activación y vuelve a la dimensión del modelo.', 'fᵢ = W₂ · activación(W₁hᵢ + b₁) + b₂', 'Vectores simbólicos', 'enc-ffn', 45, 386, 210, 38, 'Red feed-forward'],
  ['Encoder · residual y normalización', 'Otra suma residual y normalización producen la salida de esta capa. Ese resultado entra en la siguiente capa.', 'zᵢ = LayerNorm(hᵢ + fᵢ)', 'Vectores simbólicos', 'enc-out', 45, 441, 210, 38, 'Suma residual + LayerNorm'],
  ['Memoria del encoder', `Tras ${d.capas_encoder} capas se obtiene un vector contextual por token. Esta memoria se reutiliza al generar cada token de salida.`, `Z⁽${d.capas_encoder}⁾ → K, V para el decoder`, 'Vectores simbólicos · contexto de la entrada completa', 'memory', 30, 541, 240, 38, 'Memoria contextual'],
  ['Entrada del decoder', 'El decoder comienza con un token de inicio. Luego recibe los tokens previos de cada hipótesis. Aquí ilustramos el prefijo de la secuencia final, no las cuatro hipótesis.', 'inicio → inicio + primer token → …', 'Prefijo real de la salida seleccionada', 'prefix', 375, 34, 240, 35, 'Inicio / tokens previos'],
  ['Decoder · embeddings y posición', 'Los IDs del prefijo se convierten en vectores y reciben información de posición, igual que en la entrada del encoder.', 'yⱼ = embedding(IDⱼ) × escala + pⱼ', 'Vectores simbólicos del prefijo de salida', 'dec-embed', 375, 91, 240, 48, 'Embeddings + posición'],
  ['Decoder · atención causal', 'Cada posición puede atender a sí misma y a las anteriores. Una máscara bloquea las posiciones futuras.', 'A = softmax(QKᵀ / √dk + máscara)V', 'Máscara ilustrativa · visible / bloqueado', 'mask', 390, 206, 210, 38, 'Self-attention + máscara'],
  ['Decoder · residual y normalización', 'Se conserva la información del prefijo mediante la suma residual y se normaliza la salida de atención causal.', 'uⱼ = LayerNorm(yⱼ + aⱼ)', 'Vectores simbólicos', 'dec-norm1', 390, 260, 210, 38, 'Suma residual + LayerNorm'],
  ['Decoder · cross-attention', 'Las consultas Q vienen del decoder; K y V vienen de la memoria del encoder. El prefijo de salida consulta toda la entrada.', 'Q = UWq; K = ZWk; V = ZWv', 'Vectores simbólicos · conexión entre ambos bloques', 'cross', 390, 316, 210, 38, 'Cross-attention al encoder'],
  ['Decoder · residual y normalización', 'Se combina lo que llevaba el decoder con la información que acaba de consultar en el encoder.', 'vⱼ = LayerNorm(uⱼ + cⱼ)', 'Vectores simbólicos', 'dec-norm2', 390, 370, 210, 38, 'Suma residual + LayerNorm'],
  ['Decoder · feed-forward', 'Una red transforma cada vector del decoder de forma independiente, después de incorporar el contexto de entrada.', 'gⱼ = FFN(vⱼ)', 'Vectores simbólicos', 'dec-ffn', 390, 426, 210, 38, 'Red feed-forward'],
  ['Decoder · salida de la capa', `La última suma y normalización cierran la capa. La estructura se repite ${d.capas_decoder} veces antes de proyectar al vocabulario.`, 'oⱼ = LayerNorm(vⱼ + gⱼ)', 'Vectores simbólicos', 'dec-out', 390, 480, 210, 38, 'Suma residual + LayerNorm'],
  ['Probabilidades', 'El último vector del decoder se proyecta al vocabulario. Los logits permiten puntuar el siguiente token.', 'oúltimo → logits → softmax → P(siguiente token)', 'Esquema · no se capturaron probabilidades', 'logits', 375, 557, 240, 33, 'Proyección al vocabulario'],
  ['Beam search', 'Se mantienen 4 hipótesis. Cada nuevo token extiende un prefijo que vuelve al decoder; se repite hasta el criterio de parada o el límite de generación.', 'prefijo → continuaciones → 4 haces → nuevo prefijo', 'Esquema · no se reconstruyen hipótesis intermedias', 'beam', 375, 605, 240, 29, 'Beam search · 4 haces'],
  ['Texto traducido', 'La secuencia elegida se decodifica y se eliminan los tokens especiales. Mostramos un fragmento para mantener breve el recorrido.', 'IDs de salida → subpalabras → texto', 'Tokens reales de salida · no son equivalencias palabra a palabra', 'output', 375, 649, 240, 29, 'IDs → traducción']
];
let step = 0;
const get = id => document.getElementById(id);
get('sample').textContent = d.muestra_texto;
get('encoder-label').textContent = `ENCODER × ${d.capas_encoder} capas`;
get('decoder-label').textContent = `DECODER × ${d.capas_decoder} capas`;
const ns = 'http://www.w3.org/2000/svg';
steps.forEach((item, index) => {
  const [, , , , , x, y, width, height, label] = item;
  const group = document.createElementNS(ns, 'g');
  group.setAttribute('class', 'node'); group.dataset.step = index;
  const rect = document.createElementNS(ns, 'rect');
  Object.entries({x, y, width, height, rx:7}).forEach(([k,v]) => rect.setAttribute(k,v));
  const text = document.createElementNS(ns, 'text');
  text.setAttribute('x', x + width / 2); text.setAttribute('y', y + height / 2 + 4);
  text.textContent = label;
  group.append(rect, text); get('nodes').append(group);
});
const sample = d.muestra_tokens.map((token, i) => ({token, id:d.muestra_ids[i]}));
const output = d.salida_tokens.map((token, i) => ({token, id:d.salida_ids[i]}))
  .filter(item => !d.especiales.includes(item.id)).slice(0,2);
const prefix = [{token:d.salida_tokens[0], id:d.salida_ids[0]}, ...output.slice(0,1)].map((item,index) => ({...item,index}));
function table(headers, rows) {
  const table = document.createElement('table');
  [headers, ...rows].forEach((row, index) => {
    const tr = document.createElement('tr');
    row.forEach(value => {
      const cell = document.createElement(index === 0 ? 'th' : 'td');
      cell.textContent = value; tr.append(cell);
    });
    table.append(tr);
  });
  get('data').append(table);
}
function transform(items, before, after) {
  table(['Token', 'Antes', 'Después'], items.map((item,i) => [item.token, before(item,i), after(item,i)]));
}
function vector(name, i) { return `${name}${i} = [${name}${i},₁ … ${name}${i},${d.dimension}]`; }

const palette = ['#6ee7ce', '#bba2ff', '#ffc580', '#8bc9ff'];
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
let animations = [];
function svgElement(parent, tag, attrs = {}, text) {
  const el = document.createElementNS(ns, tag);
  Object.entries(attrs).forEach(([key, value]) => el.setAttribute(key, value));
  if (text !== undefined) el.textContent = text;
  parent.append(el); return el;
}
function caption(parent, x, y, text, cls = '', limit = 42) {
  const el = svgElement(parent, 'text', {x, y, class:cls, 'text-anchor':'middle'}, text.length > limit ? text.slice(0, limit - 1) + '…' : text);
  svgElement(el, 'title', {}, text); return el;
}
function cardRow(parent, items, y, mode, symbol = '', expanded = false) {
  const width = 560 / Math.max(items.length, 1);
  items.forEach((item, i) => {
    const x = 30 + i * width, color = palette[(item.index ?? i) % palette.length];
    svgElement(parent, 'rect', {x:x + 4, y, width:width - 8, height:88, rx:10, fill:'#1c2b40', stroke:color});
    caption(parent, x + width / 2, y + 27, item.token, '', Math.floor(width / 12));
    if (mode === 'vector') {
      const count = expanded ? 10 : 6, cellWidth = (width - 26) / count;
      for (let k = 0; k < count; k++) {
        svgElement(parent, 'rect', {x:x + 13 + k * cellWidth, y:y + 39, width:cellWidth - 3, height:19, rx:3,
          fill:color, opacity:[.35, .8, .5, 1, .65, .4][(k + i + (symbol.codePointAt(0) || 0)) % 6], 'data-vector':''});
      }
      caption(parent, x + width / 2, y + 77, `${symbol}${item.index ?? i}`, 'scene-small');
    } else caption(parent, x + width / 2, y + 62, `ID ${item.id}`, 'scene-small');
  });
}
function arrow(parent, path, color) {
  return svgElement(parent, 'path', {d:path, class:'scene-line', ...(color ? {style:`stroke:${color}`} : {})});
}
function operationBox(parent, title, subtitle) {
  svgElement(parent, 'rect', {x:55, y:246, width:510, height:86, rx:14, fill:'#23374c', stroke:'#6687a4'});
  caption(parent, 310, 282, title); caption(parent, 310, 311, subtitle, 'scene-small', 60);
}
function syncPlayback() {
  const running = animations.some(a => a.playState === 'running');
  get('play').textContent = running ? 'Pausar' : 'Reproducir';
  get('play').setAttribute('aria-label', running ? 'Pausar animación' : 'Reproducir animación');
  get('motion-status').textContent = running ? 'Transformación en curso' : animations.some(a => a.playState === 'paused') ? 'Animación pausada' : 'Resultado visible';
}
function playScene() {
  animations.forEach(a => { a.currentTime = 0; a.play(); }); syncPlayback();
}
function renderScene(kind) {
  animations.forEach(a => a.cancel()); animations = [];
  const scene = get('scene'); scene.replaceChildren();
  svgElement(scene, 'title', {id:'scene-title'}, steps[step][0]);
  svgElement(scene, 'desc', {id:'scene-desc'}, steps[step][1]);
  const before = svgElement(scene, 'g', {'data-phase':'before'});
  const operation = svgElement(scene, 'g', {'data-phase':'operation'});
  const after = svgElement(scene, 'g', {'data-phase':'after'});
  const decoder = step >= 9, items = (decoder ? prefix : sample).slice(0, 4);
  caption(before, 310, 32, 'ENTRADA', 'scene-label');
  caption(operation, 310, 219, 'OPERACIÓN', 'scene-label');
  caption(after, 310, 422, 'RESULTADO', 'scene-label');
  arrow(operation, 'M310 158 V193'); arrow(after, 'M310 357 V390');
  let note = 'Ilustración didáctica: las celdas representan componentes simbólicos, no valores medidos.';
  const vectorSteps = {
    embedding:['ID', 'e', 'Consultar matriz E', 'Cada ID selecciona su fila aprendida'],
    position:['e', 'x', 'Sumar posición', 'xᵢ = eᵢ + pᵢ'],
    'enc-attn':['x', 'a', 'Q · K · V', `${d.cabezas} cabezas → combinar resultados`],
    'enc-norm':['a', 'h', 'Sumar + normalizar', 'hᵢ = LayerNorm(xᵢ + aᵢ)'],
    'enc-ffn':['h', 'f', 'Expandir → activar → contraer', 'La misma red actúa en cada token'],
    'enc-out':['f', 'z', 'Sumar + normalizar', 'zᵢ = LayerNorm(hᵢ + fᵢ)'],
    memory:['z', 'Z', `${d.capas_encoder} capas del encoder`, 'Un vector contextual por token'],
    'dec-embed':['ID', 'y', 'Embedding + posición', 'yⱼ = embedding(IDⱼ) × escala + pⱼ'],
    mask:['y', 'a', 'Solo presente y pasado', 'Las posiciones futuras quedan bloqueadas'],
    'dec-norm1':['a', 'u', 'Sumar + normalizar', 'uⱼ = LayerNorm(yⱼ + aⱼ)'],
    cross:['u', 'c', 'Consultar memoria del encoder', 'Q del decoder · K y V del encoder'],
    'dec-norm2':['c', 'v', 'Sumar + normalizar', 'vⱼ = LayerNorm(uⱼ + cⱼ)'],
    'dec-ffn':['v', 'g', 'Expandir → activar → contraer', 'La misma red actúa en cada token'],
    'dec-out':['g', 'o', 'Sumar + normalizar', `oⱼ = LayerNorm(vⱼ + gⱼ) · ${d.capas_decoder} capas`]
  };
  if (vectorSteps[kind]) {
    const [input, result, title, subtitle] = vectorSteps[kind];
    cardRow(before, items, 56, input === 'ID' ? 'id' : 'vector', input);
    cardRow(after, items, 446, 'vector', result);
    if (kind.includes('norm') || kind === 'enc-out' || kind === 'dec-out') {
      caption(operation, 310, 265, title);
      caption(operation, 310, 343, subtitle, 'scene-small');
      [18, 38, 25, 45, 22, 32].forEach((height,k) => {
        svgElement(operation, 'rect', {x:210 + k * 34, y:300 - height / 2, width:25, height, rx:3,
          fill:palette[0], 'data-normalize':''});
      });
      const residual = {'enc-norm':'x', 'enc-out':'h', 'dec-norm1':'y', 'dec-norm2':'u', 'dec-out':'v'}[kind];
      svgElement(operation, 'rect', {x:35, y:168, width:195, height:33, rx:6, fill:'#3d352b', stroke:'#ffc580'});
      caption(operation, 132, 190, `Original: ${residual} · residual`, 'scene-small');
      arrow(operation, 'M35 185 H16 V236 H285', '#ffc580');
      caption(operation, 310, 241, '+', '', 5);
      note += ' El camino naranja conserva la entrada del subbloque; LayerNorm normaliza cada vector, sin mezclar tokens.';
    } else if (kind === 'position' || kind === 'dec-embed') {
      cardRow(operation, items.map((t,i) => ({token:`Posición ${i}`})), 246, 'vector', 'p');
      caption(operation, 310, 353, '+ embedding del mismo token', 'scene-small');
    } else if (kind.endsWith('ffn')) {
      cardRow(operation, items, 246, 'vector', 'activación ', true);
      caption(operation, 310, 354, 'Expandir → activar → contraer', 'scene-small');
    } else if (kind === 'enc-attn') {
      for (let i = 0; i < items.length; i++) for (let j = 0; j < items.length; j++) {
        arrow(operation, `M${70 + i * 150} 249 L${70 + j * 150} 318`, palette[i]);
      }
      caption(operation, 310, 240, 'Q · K · V de toda la entrada', 'scene-small');
      caption(operation, 310, 347, `${d.cabezas} cabezas → combinar`, 'scene-small');
      note += ' Las conexiones resumen la mezcla de información; no representan pesos de atención reales.';
    } else if (kind === 'mask') {
      const labels = ['inicio', 't₁', 't₂'];
      labels.forEach((label,i) => {
        caption(operation, 187, 261 + i * 31, label, 'scene-small');
        caption(operation, 255 + i * 63, 237, label, 'scene-small');
        labels.forEach((_,j) => {
          svgElement(operation, 'rect', {x:226 + j * 63, y:241 + i * 31, width:58, height:27, rx:4, fill:j <= i ? '#275d57' : '#283447'});
          caption(operation, 255 + j * 63, 261 + i * 31, j <= i ? '✓' : '×', 'scene-small');
        });
      });
      caption(operation, 310, 354, 'Filas: consultas · columnas: claves', 'scene-small');
      note = 'Máscara didáctica de tres posiciones: ✓ visible, × bloqueada. Los tokens futuros aún no están disponibles al generar.';
    } else if (kind === 'cross') {
      cardRow(operation, sample.slice(0, 4), 242, 'vector', 'Z');
      arrow(operation, 'M310 176 C590 175 590 240 556 269');
      caption(operation, 465, 158, 'Q consulta K, V', 'scene-small');
      caption(operation, 310, 354, 'Memoria del encoder → contexto consultado', 'scene-small');
    } else if (kind === 'embedding') {
      [0,1,2].forEach(row => {
        svgElement(operation, 'rect', {x:155, y:238 + row * 32, width:310, height:27, rx:4,
          fill:row === 1 ? '#275d57' : '#24354b', stroke:row === 1 ? palette[0] : '#34465f'});
        caption(operation, 310, 258 + row * 32, row === 1 ? 'ID → fila seleccionada → eᵢ' : '· · · · · · · · · · · ·', 'scene-small');
      });
      caption(operation, 310, 354, `Vector completo: ${d.dimension} componentes`, 'scene-small');
    } else operationBox(operation, title, subtitle);
  } else if (kind === 'text' || kind === 'tokens') {
    caption(before, 310, 107, d.muestra_texto, '', 45);
    operationBox(operation, kind === 'text' ? 'Tomar una muestra para seguirla' : 'SentencePiece → subpalabras → IDs',
      kind === 'text' ? 'El modelo traduce la entrada completa' : 'Una palabra puede ocupar varias tarjetas');
    if (kind === 'text') caption(after, 310, 492, d.muestra_texto, '', 45);
    else cardRow(after, items, 446, 'id');
    note = 'Datos reales: muestra de las dos primeras palabras y sus tokens e IDs, tokenizados por separado.';
  } else if (kind === 'prefix') {
    cardRow(before, prefix.slice(0,1), 56, 'id');
    operationBox(operation, 'Añadir el token generado al prefijo', 'El prefijo vuelve a entrar al decoder');
    cardRow(after, prefix, 446, 'id');
    note = 'Datos reales de la secuencia elegida. Se ilustra su primer prefijo; cada hipótesis mantiene el suyo.';
  } else if (kind === 'logits') {
    cardRow(before, prefix.slice(-1), 56, 'vector', 'o');
    operationBox(operation, 'Proyectar al vocabulario → softmax', 'Un logit por token → distribución de probabilidad');
    [0.72, 0.46, 0.25].forEach((value,i) => {
      caption(after, 124, 457 + i * 37, `Candidato ${'ABC'[i]}`, 'scene-small');
      svgElement(after, 'rect', {x:205, y:440 + i * 37, width:value * 430, height:23, rx:5, fill:palette[i], 'data-vector':''});
    });
    note = 'Ilustración didáctica: alturas relativas de ejemplo, sin probabilidades capturadas ni candidatos reales.';
  } else if (kind === 'beam') {
    caption(before, 310, 107, 'Prefijos de las hipótesis actuales');
    [0,1,2,3].forEach(i => {
      const x = 85 + i * 150;
      arrow(operation, `M310 236 L${x} 280`, palette[i]);
      svgElement(operation, 'rect', {x:x - 57, y:282, width:114, height:54, rx:9, fill:'#24354b', stroke:palette[i]});
      caption(operation, x, 315, `Haz ${i + 1}`);
      arrow(after, `M${x} 338 V389`, palette[i]);
    });
    caption(after, 310, 470, 'Conservar 4 continuaciones candidatas');
    caption(after, 310, 507, 'Nuevo prefijo ↺ decoder', 'scene-small');
    note = 'Esquema didáctico de beam search: no son las hipótesis ni las puntuaciones de esta traducción.';
  } else if (kind === 'output') {
    cardRow(before, output, 56, 'id');
    operationBox(operation, 'Decodificar y quitar tokens especiales', 'Las subpalabras se unen para formar texto');
    caption(after, 310, 492, d.traduccion, '', 45);
    note = 'Datos reales: primeros tokens de salida y traducción final. El texto completo sigue visible en la aplicación.';
  }
  if (sample.length > 4 && !decoder) note += ` Se muestran 4 de ${sample.length} tokens; la atención utiliza toda la entrada.`;
  get('scene-note').textContent = note;
  // Tres fases finitas: la escena termina con el resultado a la vista.
  [before, operation, after].forEach((group,i) => {
    const a = group.animate([{opacity:0, transform:'translateY(14px)'}, {opacity:1, transform:'translateY(0)'}],
      {duration:800, delay:i * 1300, fill:'both', easing:'ease-out'});
    a.playbackRate = Number(get('speed').value); a.onfinish = syncPlayback; animations.push(a);
  });
  scene.querySelectorAll('[data-vector]').forEach(cell => {
    cell.style.transformBox = 'fill-box'; cell.style.transformOrigin = 'left center';
    const delay = cell.closest('[data-phase]').dataset.phase === 'after' ? 2600 : cell.closest('[data-phase]').dataset.phase === 'operation' ? 1300 : 0;
    const a = cell.animate([{transform:'scaleX(.1)'}, {transform:'scaleX(1)'}], {duration:800, delay, fill:'both'});
    a.playbackRate = Number(get('speed').value); animations.push(a);
  });
  scene.querySelectorAll('.scene-line, [data-normalize]').forEach(el => {
    const normalizing = el.hasAttribute('data-normalize');
    el.style.transformBox = 'fill-box'; el.style.transformOrigin = 'center';
    const length = normalizing ? 0 : el.getTotalLength();
    if (!normalizing) el.style.strokeDasharray = length;
    const frames = normalizing ? [{transform:'scaleY(1)'}, {transform:'scaleY(.6)'}] : [{strokeDashoffset:length}, {strokeDashoffset:0}];
    const delay = el.closest('[data-phase]').dataset.phase === 'after' ? 2200 : 1000;
    const a = el.animate(frames, {duration:800, delay, fill:'both', easing:'ease-in-out'});
    a.playbackRate = Number(get('speed').value); animations.push(a);
  });
  if (reducedMotion.matches) animations.forEach(a => a.finish());
  syncPlayback();
}
get('play').addEventListener('click', () => {
  if (animations.some(a => a.playState === 'running')) animations.forEach(a => a.pause());
  else if (animations.some(a => a.playState === 'paused')) animations.forEach(a => a.play());
  else playScene();
  syncPlayback();
});
get('replay').addEventListener('click', playScene);
get('speed').addEventListener('change', () => animations.forEach(a => a.updatePlaybackRate(Number(get('speed').value))));
reducedMotion.addEventListener('change', () => { if (reducedMotion.matches) { animations.forEach(a => a.finish()); syncPlayback(); } });

function render() {
  const [title, description, formula, representation, kind] = steps[step];
  get('counter').textContent = `${step + 1} / ${steps.length}`;
  get('stage').textContent = step >= 4 && step <= 8 ? 'Dentro del encoder' : step >= 10 && step <= 16 ? 'Dentro del decoder' : 'Flujo de datos';
  get('progress').style.width = `${(step + 1) / steps.length * 100}%`;
  get('title').textContent = title; get('description').textContent = description;
  get('formula').textContent = formula; get('representation').textContent = representation;
  get('data').replaceChildren();
  const transforms = {
    embedding: [sample, (t,i)=>`ID ${t.id}`, (t,i)=>vector('e',i)],
    position: [sample, (t,i)=>`e${i} + p${i}`, (t,i)=>vector('x',i)],
    'enc-attn': [sample, (t,i)=>`x${i} → q${i}, k${i}, v${i}`, (t,i)=>`a${i} = mezcla de V de toda la entrada`],
    'enc-norm': [sample, (t,i)=>`x${i} + a${i}`, (t,i)=>vector('h',i)],
    'enc-ffn': [sample, (t,i)=>vector('h',i), (t,i)=>vector('f',i)],
    'enc-out': [sample, (t,i)=>`h${i} + f${i}`, (t,i)=>vector('z',i)],
    memory: [sample, (t,i)=>`z${i} de la primera capa`, (t,i)=>`z${i}⁽${d.capas_encoder}⁾ contextual`],
    'dec-embed': [prefix, (t,i)=>`ID ${t.id} + posición ${i}`, (t,i)=>vector('y',i)],
    'dec-norm1': [prefix, (t,i)=>`y${i} + a${i}`, (t,i)=>vector('u',i)],
    cross: [prefix, (t,i)=>`q${i} del decoder + K, V del encoder`, (t,i)=>`c${i} = contexto consultado en la entrada`],
    'dec-norm2': [prefix, (t,i)=>`u${i} + c${i}`, (t,i)=>vector('v',i)],
    'dec-ffn': [prefix, (t,i)=>vector('v',i), (t,i)=>vector('g',i)],
    'dec-out': [prefix, (t,i)=>`v${i} + g${i}`, (t,i)=>vector('o',i)]
  };
  if (transforms[kind]) transform(...transforms[kind]);
  else if (kind === 'text') get('data').textContent = d.muestra_texto;
  else if (kind === 'tokens') table(['Subpalabra', 'ID'], sample.map(t=>[t.token,t.id]));
  else if (kind === 'prefix') table(['Posición', 'Token de entrada del decoder', 'ID'], prefix.map((t,i)=>[i,t.token,t.id]));
  else if (kind === 'mask') table(['Consulta ↓ / Clave →', ...prefix.map(t=>t.token)], prefix.map((t,i)=>[t.token,...prefix.map((_,j)=> j<=i ? 'Visible' : 'Bloqueado')]));
  else if (kind === 'logits') get('data').textContent = `${d.dimension} componentes → un logit por token del vocabulario → puntuaciones de continuación.`;
  else if (kind === 'beam') get('data').textContent = 'Las 4 hipótesis comparten la memoria del encoder, pero cada una tiene su propio prefijo de salida.';
  else if (kind === 'output') {
    const text = document.createElement('p'); text.textContent = d.traduccion.split(/\s+/).slice(0,2).join(' ');
    get('data').append(text); table(['Primeros tokens de salida', 'ID'], output.map(t=>[t.token,t.id]));
  }
  renderScene(kind);
  get('data').scrollTop = 0;
  document.querySelectorAll('[data-step]').forEach(el => {
    el.classList.toggle('active', Number(el.dataset.step) === step);
    el.classList.toggle('done', Number(el.dataset.step) < step);
  });
  get('prev').disabled = step === 0; get('next').disabled = step === steps.length - 1;

}
function move(delta) { step = Math.max(0, Math.min(steps.length - 1, step + delta)); render(); }
get('prev').addEventListener('click', () => move(-1));
get('next').addEventListener('click', () => move(1));
document.addEventListener('keydown', event => {
  if (event.target.closest('#data, select, button, summary')) return;
  if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
    event.preventDefault(); move(event.key === 'ArrowRight' ? 1 : -1);
  }
});
render();
</script>
</body>
</html>'''
