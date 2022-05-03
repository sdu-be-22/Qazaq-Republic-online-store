console.log(document.cookie)
console.log('starting from here')

let cart = JSON.parse(get_cookie('cart'))
console.log(cart, 'this is cart')

if (cart == undefined) {
    console.log('are you here')
    cart = {}
    console.log('cart was created')
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
}
