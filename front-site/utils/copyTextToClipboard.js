const fallbackCopyTextToClipboard = (text) => {
  const textArea = document.createElement('textarea')
  textArea.value = text

  textArea.style.top = '0'
  textArea.style.left = '0'
  textArea.style.position = 'fixed'

  document.body.appendChild(textArea)
  textArea.focus()
  textArea.select()

  try {
    const successful = document.execCommand('copy')
    document.body.removeChild(textArea)
    return successful ? '' : ''
  } catch (err) {
    document.body.removeChild(textArea)
    return ''
  }
}

export default async (text) => {
  return await new Promise((resolve) => {
    if (!navigator.clipboard) {
      return resolve(fallbackCopyTextToClipboard(text))
    }

    navigator.clipboard.writeText(text)
      .then(() => {
        resolve()
      }, (_) => {
        resolve()
      })
  })
}
