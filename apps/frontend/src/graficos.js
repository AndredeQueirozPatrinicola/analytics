import { Chart } from "chart.js/auto";
import pegaApi from './api';
import ChartjsPluginStacked100 from "chartjs-plugin-stacked100";

Chart.register(ChartjsPluginStacked100);

const DEFAULT_PARAMS = {
  ano_inicial: 2017,
  ano_final: 2022,
  departamento: ""
}

async function formataParametros(parameters) {
  if (parameters.length === 4) {
    return {
      "stacked": parameters[0],
      "ano_inicial": parameters[1],
      "ano_final": parameters[2],
      "departamento": parameters[3],
    }
  }
  else if (parameters.length === 3) {
    return {
      "stacked": parameters[0],
      "ano": parameters[1],
      "departamento": parameters[2]
    }
  }
  else if (parameters.length === 1) {
    return {
      "departamento": parameters[0]
    }
  }
}

async function raiseDataError(ctx) {
  ctx.classList.add('active-message')
}

async function plotaGrafico(element, parameters) {

  let chart = Chart.getChart(element.id)
  if (!chart) {
    const config = await pegaApi(element, DEFAULT_PARAMS)
    element.classList.remove('hide')
    const loader = element.parentElement.children[1]
    loader.classList.remove('show')
    new Chart(element, config)
  }
  else {
    chart.destroy()
    const config = await pegaApi(element, parameters)
    element.classList.remove('hide')
    const loader = element.parentElement.children[1]
    loader.classList.remove('show')
    new Chart(element, config)
  }
}

async function submitPost(element) {
  const message = element.parentElement.parentElement.firstElementChild;
  const parent = element.parentElement;
  const chart = Array.from(parent.parentElement.children).filter(element => element.className == 'grafico-container')[0].firstElementChild;
  const loader = chart.parentElement.children[1]
  const selectContainer = Array.from(parent.children)

  message.classList.remove('active-message')
  chart.classList.add('hide')
  loader.classList.add('show')

  let parametros = []
  selectContainer.map((tag) => {
    let parametro = tag.children[1] ? tag.children[1] : false;
    if (parametro.tagName === 'INPUT') {
      parametros.push(parametro.checked);
    }
    else if (parametro.tagName === 'SELECT') {
      parametros.push(parametro.value);
    }

  })

  parametros = await formataParametros(parametros);

  if (parametros.ano_inicial > parametros.ano_final) {
    raiseDataError(message)
  }
  else {
    plotaGrafico(chart, parametros)
  }
}

export async function coordenaGraficos() {
  const graficos = Array.from(document.getElementsByTagName('canvas'))
  graficos.forEach(tag => {
    plotaGrafico(tag)
  });
  const selectButtons = Array.from(document.getElementsByTagName('btn'))
  selectButtons.forEach(tag => {
    tag.addEventListener('click', () => {
      submitPost(tag);
    });
  })
}