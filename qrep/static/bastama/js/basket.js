function add_product_to_basket(product_data) {
  let selected_size = document.querySelector('.selector-item_radio:checked')
  let selected_color = document.querySelector('.active-color')
  let quantity = document.querySelector("input[name=quantity]")

  selected_size = selected_size == undefined ? null : selected_size.value
  selected_color = selected_color == undefined ? null : selected_color.value
  quantity = quantity == undefined ? null : quantity.value

  if (user === 'AnonymousUser') {
    window.location.href = '/account/login'
  } else {
    authenticated_user_basket(selected_size, selected_color, product_data, quantity)
  }
}

function authenticated_user_basket(size, color, product_data, quantity) {
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
      location.reload()
    })
    .catch(err => {
      console.error(err)
    })
}

let updateBtns = document.getElementsByClassName('chg-quantity')

for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        let productId = this.dataset.product
        let action = this.dataset.action

        if (user !== 'AnonymousUser') {
          updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action) {
    console.log('User is logged in, sending data')

    const url = '/update_item/'
    const csrftoken = get_cookie('csrftoken')

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            console.log(data)
            location.reload()
        })
}