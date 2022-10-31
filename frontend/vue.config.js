module.exports = {
  devServer: {
    proxy: {
      '^/api': {
        target: 'http://0.0.0.0:5000'
      },
      '^/uploads': {
        target: 'http://0.0.0.0:5000'
      }
    }
  }
}
