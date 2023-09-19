export function useHeaderToken () {
  const token = getToken('csrftoken')

  if (token) {
    return {
      'X-CSRFToken': token,
    }
  }

  return {}
}

function getToken (name: string) {
  let cookieValue = null
  if (document && document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }

  return cookieValue
}
