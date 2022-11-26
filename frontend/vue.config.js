const back = 'http://0.0.0.0:5000/' // 'http://wb.nio.design'
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
