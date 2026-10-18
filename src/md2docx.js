/**
 * Convierte un Markdown sencillo (títulos #/##/###, párrafos, **negritas**, *cursivas*, `código`,
 * listas con - o 1., tablas con |) a .docx con estilos legibles. Pensado para los entregables del
 * reto (informe, bibliografía, anexos).
 *
 * Uso:  node src/md2docx.js entrada.md salida.docx ["Título de portada"]
 * Requiere el paquete npm `docx` (se busca en NODE_PATH o junto al script).
 */
const fs = require('fs')
const path = require('path')
const {
  AlignmentType, BorderStyle, Document, HeadingLevel, LevelFormat, Packer, Paragraph, ShadingType,
  Table, TableCell, TableRow, TextRun, WidthType,
} = require('docx')

const [, , entrada, salida, tituloPortada] = process.argv
if (!entrada || !salida) {
  console.error('Uso: node md2docx.js entrada.md salida.docx ["Título"]')
  process.exit(1)
}
const md = fs.readFileSync(entrada, 'utf8').replace(/\r\n/g, '\n')
const FUENTE = 'Calibri'
const ANCHO = 9026 // ancho útil en DXA (carta, márgenes de 1")

// ---- inline: **negrita**, *cursiva*, `código`
function runs(texto, extra = {}) {
  const out = []
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/g
  let ult = 0
  let m
  while ((m = re.exec(texto))) {
    if (m.index > ult) out.push(new TextRun({ text: texto.slice(ult, m.index), font: FUENTE, ...extra }))
    const t = m[0]
    if (t.startsWith('**')) out.push(new TextRun({ text: t.slice(2, -2), bold: true, font: FUENTE, ...extra }))
    else if (t.startsWith('`')) out.push(new TextRun({ text: t.slice(1, -1), font: 'Consolas', size: 20, ...extra }))
    else out.push(new TextRun({ text: t.slice(1, -1), italics: true, font: FUENTE, ...extra }))
    ult = m.index + t.length
  }
  if (ult < texto.length) out.push(new TextRun({ text: texto.slice(ult), font: FUENTE, ...extra }))
  return out
}

const parrafo = (texto, opts = {}) =>
  new Paragraph({ children: runs(texto), spacing: { after: 140, line: 288 }, alignment: AlignmentType.JUSTIFIED, ...opts })

function tabla(filas) {
  const celdas = filas.map((f) => f.split('|').slice(1, -1).map((c) => c.trim()))
  const cuerpo = celdas.filter((f, i) => !(i === 1 && f.every((c) => /^:?-+:?$/.test(c))))
  const nCol = Math.max(...cuerpo.map((f) => f.length))
  // ancho proporcional al texto más largo de cada columna (mínimo 8 %, máximo 60 %)
  const largo = Array.from({ length: nCol }, (_, j) =>
    Math.min(60, Math.max(8, Math.max(...cuerpo.map((f) => (f[j] ?? '').length)))))
  const suma = largo.reduce((a, b) => a + b, 0)
  const anchos = largo.map((l) => Math.floor((ANCHO * l) / suma))
  anchos[nCol - 1] += ANCHO - anchos.reduce((a, b) => a + b, 0)
  return new Table({
    width: { size: ANCHO, type: WidthType.DXA },
    columnWidths: anchos,
    rows: cuerpo.map((f, i) =>
      new TableRow({
        tableHeader: i === 0,
        children: Array.from({ length: nCol }, (_, j) =>
          new TableCell({
            width: { size: anchos[j], type: WidthType.DXA },
            shading: i === 0 ? { type: ShadingType.CLEAR, fill: 'E8F0E3' } : undefined,
            margins: { top: 40, bottom: 40, left: 80, right: 80 },
            children: [new Paragraph({ children: runs(f[j] ?? '', { size: 19, bold: i === 0 }), spacing: { after: 0 } })],
          }),
        ),
      }),
    ),
  })
}

const hijos = []
if (tituloPortada) {
  hijos.push(new Paragraph({ children: [new TextRun({ text: tituloPortada, bold: true, size: 36, font: FUENTE })], spacing: { after: 240 }, alignment: AlignmentType.CENTER }))
}

const lineas = md.split('\n')
let i = 0
let parrafoAcum = []
const vaciar = () => {
  if (parrafoAcum.length) {
    hijos.push(parrafo(parrafoAcum.join(' ')))
    parrafoAcum = []
  }
}
while (i < lineas.length) {
  const l = lineas[i]
  if (/^#{1,3} /.test(l)) {
    vaciar()
    const nivel = l.match(/^#+/)[0].length
    const texto = l.replace(/^#+ /, '').replace(/\s*\[[^\]]*palabras[^\]]*\]/, '').replace(/\s*\(máx\. 4 cuartillas;[^)]*\)/, '')
    if (nivel === 1 && tituloPortada) { i++; continue }
    hijos.push(new Paragraph({
      heading: nivel === 1 ? HeadingLevel.TITLE : nivel === 2 ? HeadingLevel.HEADING_1 : HeadingLevel.HEADING_2,
      children: [new TextRun({ text: texto, font: FUENTE, bold: true, color: '2F4F1F', size: nivel === 1 ? 32 : nivel === 2 ? 28 : 24 })],
      spacing: { before: 280, after: 120 },
    }))
    i++
  } else if (/^---+$/.test(l.trim())) {
    vaciar(); i++
  } else if (/^\|/.test(l)) {
    vaciar()
    const filas = []
    while (i < lineas.length && /^\|/.test(lineas[i])) filas.push(lineas[i++])
    hijos.push(tabla(filas), new Paragraph({ spacing: { after: 120 } }))
  } else if (/^(\s*)([-*]|\d+\.) /.test(l)) {
    vaciar()
    while (i < lineas.length && /^(\s*)([-*]|\d+\.) /.test(lineas[i])) {
      const m = lineas[i].match(/^(\s*)([-*]|\d+\.) (.*)$/)
      let texto = m[3]
      i++
      while (i < lineas.length && /^\s{2,}\S/.test(lineas[i]) && !/^\s*([-*]|\d+\.) /.test(lineas[i])) texto += ' ' + lineas[i++].trim()
      const numerada = /\d/.test(m[2])
      hijos.push(new Paragraph({
        children: runs(texto),
        numbering: { reference: numerada ? 'num' : 'vineta', level: 0 },
        spacing: { after: 80, line: 276 },
        alignment: AlignmentType.JUSTIFIED,
      }))
    }
  } else if (l.trim() === '') {
    vaciar(); i++
  } else if (/^<!--/.test(l.trim())) {
    i++
  } else {
    parrafoAcum.push(l.trim()); i++
  }
}
vaciar()

const doc = new Document({
  creator: 'Equipo CebadaVision',
  title: tituloPortada || path.basename(salida, '.docx'),
  styles: { default: { document: { run: { font: FUENTE, size: 22 } } } },
  numbering: {
    config: [
      { reference: 'vineta', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] },
      { reference: 'num', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] },
    ],
  },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    children: hijos,
  }],
})

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(salida, buf)
  console.log(`Escrito ${salida} (${hijos.length} bloques)`)
})
