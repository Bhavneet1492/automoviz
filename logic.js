let theme = document.getElementById("thm");
let css = document.getElementById("css");
let favicon = document.getElementById("favicon");
let sun = document.getElementById("sun");
let car = document.getElementById("car");
let Top = document.getElementById("Top");
let clicked = false;
theme.addEventListener("click", () => {
  if (clicked == true) {
    clicked = false;
    css.href = "style2.css";
    favicon.href = "./images/index/style2/logo.svg";
    sun.style.display = "none";
    car.src = "./images/index/style2/car.svg";
    theme.innerHTML = "serene";
    Top.display = "block";
  } else {
    clicked = true;
    css.href = "style.css";
    favicon.href = "./images/index/style/logo.svg";
    sun.style.display = "flex";
    car.src = "./images/index/style/car.svg";
    theme.innerHTML = "classic";
    Top.display = "none";
  }
});
