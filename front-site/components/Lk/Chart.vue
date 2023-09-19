<template>
  <Line
    :data="chartData"
    :options="chartOptions"
  />
</template>

<script setup>
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Filler,
  TimeScale,
} from 'chart.js'
import { Line } from 'vue-chartjs'
import 'chartjs-adapter-date-fns'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Filler,
  TimeScale,
)

// let width, height, gradient
// function getGradient (ctx, chartArea, colors) {
//   const chartWidth = chartArea.right - chartArea.left
//   const chartHeight = chartArea.bottom - chartArea.top
//   if (!gradient || width !== chartWidth || height !== chartHeight) {
//     width = chartWidth
//     height = chartHeight
//     gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top)
//     gradient.addColorStop(1, colors[0])
//     gradient.addColorStop(0, colors[1])
//   }

//   return gradient
// }

const getOrCreateTooltip = (chart) => {
  let tooltipEl = chart.canvas.parentNode.querySelector('div')

  if (!tooltipEl) {
    tooltipEl = document.createElement('div')
    tooltipEl.style.width = '260px'
    tooltipEl.style.display = 'flex'
    tooltipEl.style.flexDirection = 'column'
    tooltipEl.style.background = '#18181C'
    tooltipEl.style.borderRadius = '8px'
    tooltipEl.style.color = 'white'
    tooltipEl.style.opacity = 1
    tooltipEl.style.fontSize = '12px'
    tooltipEl.style.lineHeight = '14px'
    tooltipEl.style.pointerEvents = 'none'
    tooltipEl.style.position = 'absolute'
    tooltipEl.style.transform = 'translate(-50%, 0)'
    tooltipEl.style.transition = 'all .1s ease'
    tooltipEl.style.boxShadow = '0px 2px 8px rgba(44, 48, 64, 0.2)'

    const content = document.createElement('div')
    content.classList.add('tooltip-content')

    tooltipEl.appendChild(content)
    chart.canvas.parentNode.appendChild(tooltipEl)
  }

  return tooltipEl
}

const externalTooltipHandler = (context) => {
  // Tooltip Element
  const { chart, tooltip } = context
  const tooltipEl = getOrCreateTooltip(chart)

  // Hide if no tooltip
  if (tooltip.opacity === 0) {
    tooltipEl.style.opacity = 0
    return
  }

  // Set Text
  if (tooltip.body) {
    const title = tooltip.title || []
    const dataPoints = tooltip.dataPoints

    const contentTitle = document.createElement('p')
    contentTitle.style.color = '#9D9DA5'

    if (title && title[0]) {
      const date = new Date(title[0] * 1000).toLocaleString('ru', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        timezone: 'UTC',
      }).replace(' г.', '')
      const contentText = document.createTextNode(date)
      contentTitle.appendChild(contentText)
    }

    const contentBody = document.createElement('div')
    contentBody.style.display = 'flex'
    contentBody.style.flexDirection = 'column'

    dataPoints.forEach((item) => {
      const contentLine = document.createElement('div')
      contentLine.style.width = '100%'
      contentLine.style.display = 'flex'
      contentLine.style.alignItems = 'center'
      contentLine.style.justifyContent = 'space-between'
      contentLine.style.marginTop = '12px'
      const contentLabel = document.createElement('span')
      const contentLabelText = document.createTextNode(item.dataset.label)
      contentLabel.appendChild(contentLabelText)
      const contentValue = document.createElement('span')
      const contentValueText = document.createTextNode(item.formattedValue + ` ${item.dataset.valueSuffix}`)
      contentValue.appendChild(contentValueText)

      contentLine.appendChild(contentLabel)
      contentLine.appendChild(contentValue)
      contentBody.appendChild(contentLine)
    })

    const tableRoot = tooltipEl.querySelector('.tooltip-content')

    // Remove old children
    while (tableRoot.firstChild) {
      tableRoot.firstChild.remove()
    }

    // Add new children
    tableRoot.appendChild(contentTitle)
    tableRoot.appendChild(contentBody)
  }

  const { offsetLeft: positionX, offsetTop: positionY } = chart.canvas

  // Display, position, and set styles for font
  tooltipEl.style.opacity = 1
  tooltipEl.style.left = positionX + tooltip.caretX + 'px'
  tooltipEl.style.top = positionY + tooltip.caretY + 'px'
  tooltipEl.style.padding = '12px 16px 16px'
}

const props = defineProps({
  data: {
    type: Object,
    default: () => ({}),
  },
  options: {
    type: Object,
    default: () => ({}),
  },
})

const defaultData = {
  labels: [],
  datasets: [],
}

const defaultOptions = {
  responsive: true,
  maintainAspectRatio: false,
  parsing: {
    xAxisKey: 'x',
    yAxisKey: 'y',
  },
  plugins: {
    legend: false,
    tooltip: {
      enabled: false,
      position: 'nearest',
      external: externalTooltipHandler,
    },
  },
  datasets: {
    line: {
      borderWidth: 2,
    },
  },
  elements: {
    point: {
      pointBorderWidth: 2,
      backgroundColor: '#fff',
    },
  },
  interaction: {
    position: 'nearest',
    intersect: false,
    mode: 'index',
  },
  scales: {
    x: {
      display: true,
      type: 'time',
      offset: false,
      time: {
        displayFormats: {
          quarter: 'DD MMM',
        },
        unit: 'day',
        tooltipFormat: 't',
      },
    },
    y: {
      grid: {
        display: false,
      },
      beginAtZero: true,
    },
  },
  animation: {
    duration: 0,
  },
  hover: {
    axis: 'xy',
    animationDuration: 0,
  },
  responsiveAnimationDuration: 0,
}

const chartData = computed(() => {
  return {
    ...defaultData,
    ...props.data,
  }
})

const chartOptions = computed(() => {
  return {
    ...defaultOptions,
    ...props.options,
  }
})
</script>
