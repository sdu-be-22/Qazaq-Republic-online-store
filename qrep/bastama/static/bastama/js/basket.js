function add_product_to_basket(product_data) {
  let selected_size = document.querySelector('.selector-item_radio:checked')
  let selected_color = document.querySelector('.active-color')
  let quantity = document.querySelector("input[name=quantity]")

  if (user === 'AnonymousUser') {
    console.log(user, 'not authenticated')
  } else {
    authenticated_user_request(selected_size.value, selected_color.value, product_data, quantity.value)
  }
}

function authenticated_user_request(size, color, product_data, quantity) {
  const url = '/basket_add/'
  const csrf_token = get_cookie('csrftoken')

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf_token,
    },
    body: JSON.stringify({'size': size, 'color': color, 'quantity': quantity, 'product': product_data})
  })
    .then(res => res.json())
    .then(data => {
      console.log(data)
      location.reload()
    })
    .catch(err => {
      console.error(err)
    })

}