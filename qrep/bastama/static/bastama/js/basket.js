console.log(document.cookie)
console.log('starting from here')

function get_cookie(name) {
    let cookieArr = document.cookie
    console.log(cookieArr)

    for (let i = 0; i < cookieArr.length; i++) {
        let cookiePair = cookieArr[i].split('=')

        if (cookiePair[0] === name) {
            return decodeURIComponent(cookiePair[1])
        }
    }
    return null
}

let cart = JSON.parse(get_cookie('cart'))
console.log(cart, 'this is cart')

if (cart == undefined) {
    console.log('are you here')
    cart = {}
    console.log('cart was created')
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
}