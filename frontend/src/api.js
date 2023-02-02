import axios from 'axios';

function getToken(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

export const api = {

  async getMe () {
    return axios.get('/api/auth/me')
  },

  async login (context) {
    return axios.post('/api/auth/log_in', {
      username: context.state.user.username,
      password: context.state.user.password,
    }, {
      headers: {
        'X-CSRFToken': getToken('csrftoken')
      }
    })
  },

  async signup (context) {
    return axios.post('/api/auth/signup', context.state.user, {
      headers: {
        'X-CSRFToken': getToken('csrftoken')
      }
    })
  },

  async logout () {
    return axios.post('/api/auth/log_out', {}, {
      headers: {
        'X-CSRFToken': getToken('csrftoken')
      }
    })
  },

  async getData () {
    return axios.get('/api/data')
  },

  async getProducts (context) {
    return axios.get('/api/products', {params: context.state.params})
  },

  async getTopCategories (context) {
    return axios.get('/api/top', {params: context.state.topCategoriesParams})
  },

  async getCategories () {
    return axios.get('/api/categories')
  },

  async getCategory (context, id) {
    return axios.get(`/api/categories/${id}`, {params: context.state.categoryParams})
  },

  async saveCategory (context) {
    return axios.post(`/api/categories`, {
      id: context.state.category._id ? context.state.category._id.$oid : null,
      name: context.state.category.name,
    })
  },

  async deleteCategory (context) {
    return axios.delete(`/api/categories/${context.state.category._id.$oid}`)
  },

}
