// const back = 'http://0.0.0.0:5000/'
const back = 'https://spotter.fun'
module.exports = {
  devServer: {
    proxy: {
      '^/api/auth': {
        target: 'http://0.0.0.0:8000/'
      },
      '^/api/accounts': {
        target: 'http://0.0.0.0:8000/'
      },
      '^/api': {
        target: back
      },
      '^/uploads': {
        target: back
      }
    }
  }
}
