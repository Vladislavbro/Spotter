// const back = 'http://0.0.0.0:5000/'
const back = 'https://spotter.fun'
module.exports = {
  devServer: {
    proxy: {
      '^/api': {
        target: back
      },
      '^/uploads': {
        target: back
      }
    }
  }
}
