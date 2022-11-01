module.exports = {
  devServer: {
    proxy: {
      '^/api': {
        target: 'http://wb.nio.design'
      },
      '^/uploads': {
        target: 'http://wb.nio.design/'
      }
    }
  }
}
