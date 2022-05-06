function big(element){
    element.style.fontSize = "50px";
}

function small(element){
    element.style.fontSize="45px";
}
function change(element){
    var a = element.innerHTML;
    switch(a){
        case "-Almaty-":
            document.getElementById("map").src="static/bastama/images/home/almaty.png";
            document.getElementById("h").innerHTML="meken-jai: Almaty, Mametova 47 & Rozybakieva 247a";
            document.getElementById("t").innerHTML="+7‒708‒688‒61‒18 || +7‒778‒948‒98‒00";
            break;
        case "-Nur-Sultan-":
            document.getElementById("map").src="static/bastama/images/home/astana.png";
            document.getElementById("qala").href="whatsapp://send?phone=77081223910&text=";
            document.getElementById("h").innerHTML="meken-jai: Nur-Sultan, Uly Dala 7/7 & Qabanbai Batyr 62";
            document.getElementById("t").innerHTML="+7‒777‒062‒13‒09";
            break;
        case "-Shymkent-":
            document.getElementById("map").src="static/bastama/images/home/shym.png";
            document.getElementById("qala").href="whatsapp://send?phone=77088001465&text=";
            document.getElementById("h").innerHTML="meken-jai: Shymkent, Tauke khan 43a";
            document.getElementById("t").innerHTML=" ";
           break;
        case "-Aqtobe-":
            document.getElementById("map").src="static/bastama/images/home/aqtobe.png";
            document.getElementById("qala").href="whatsapp://send?phone=77088001465&text=";
            document.getElementById("h").innerHTML="meken-jai: Aqtobe, Mametova 4";
            document.getElementById("t").innerHTML="+7‒7132-77-70-78";
           break;
        case "-Aqtau-":
            document.getElementById("map").src="static/bastama/images/home/aqtau.png";
            document.getElementById("qala").href="whatsapp://send?phone=77088001465&text=";
            document.getElementById("h").innerHTML="meken-jai: Aqtau, 17 mkr. 95";
            document.getElementById("t").innerHTML="+7‒778‒546‒07‒83";
            break;
    }

}

let sidebar = document.querySelector('#sidebar');
let hamburger = document.querySelector('.hamburger')

function openSide () {
    if (sidebar.classList.contains('active')) {
        sidebar.classList.remove('active')
        hamburger.classList.remove('open')
    } else {
        sidebar.classList.add('active')
        hamburger.classList.add('open')
    }
}


// Clicking Favorite button logic

$('.click').click(function() {
  if ($('span').hasClass("fa-star")) {
    click_like_to_product('remove', this.dataset.product)

    $('.click')
      $('.click').removeClass('active')
    setTimeout(function() {
      $('.click').removeClass('active-2')
    }, 30)
      $('.click').removeClass('active-3')
    setTimeout(function() {
      $('.click span').removeClass('fa-star')
      $('.click span').addClass('fa-star-o')
    }, 15)
  } else {
    click_like_to_product('add', this.dataset.product)

    $('.click').addClass('active')
    $('.click').addClass('active-2')
    setTimeout(function() {
      $('.click span').addClass('fa-star')
      $('.click span').removeClass('fa-star-o')
    }, 150)
    setTimeout(function() {
      $('.click').addClass('active-3')
    }, 150)
    $('.info').addClass('info-tog')
    setTimeout(function(){
      $('.info').removeClass('info-tog')
    },1000)
  }
})


// Fetch request to the server after clicking like
function click_like_to_product(action, product_slug) {
  const url = '/update_like/'
  const csrf_token = get_cookie('csrftoken')

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf_token,
    },
    body: JSON.stringify({'action': action, 'product_slug': product_slug})
  })
    .then(res => {
      if (res.status === 401) {
        window.location.href = '/account/login'
      }
      return res.json()
    })
    .then(data => {
      console.log(data)
    })
    .catch(err => {
      console.error(err)
    })
}


// Adding active-color to tag
function active_color(element) {
  let color_buttons = $('.butselectcolf')

  for (let color of color_buttons) {
    color.classList.remove('active-color')
  }

  element.classList.add('active-color')
}

// Counter quantity increase or decrease
function increaseCount(a, b) {
  var input = b.previousElementSibling;
  var value = parseInt(input.value, 10);
  value = isNaN(value) ? 0 : value;
  value++;
  input.value = value;
}



function decreaseCount(a, b) {
  var input = b.nextElementSibling;
  var value = parseInt(input.value, 10);
  if (value > 1) {
    value = isNaN(value) ? 0 : value;
    value--;
    input.value = value;
  }
}

Vue.use(VueMaterial.default)

        var example = {
            methods:{
                download: function(){
                    let email = document.getElementById("emailAddress");
                    let fullname = document.getElementById("messagee");
                    let mes = document.getElementById("message");

                    let data = "Question from user " + "\n" +
                    "\nEmail: " + email.value + "\n " +
                    "\nFullname: " + fullname.value + "\n" +
                    "\nMessage: " + mes.value + "\n " ;


                    var blob = new Blob([ data ], { "type" : "text/plain" });
                    let link = document.createElement('a')
                    link.href = window.URL.createObjectURL(blob)
                    link.download = 'information.txt'
                    link.click()
                }
            }
        }

        var app = new Vue(example)

        app.$mount("#app");


