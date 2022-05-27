let theme = document.getElementById("thm");
let n = document.getElementById("css");
let sun = document.getElementById("sun");
let car = document.getElementById("car");
let Top = document.getElementById("Top");
let clicked = false;
theme.addEventListener("click", () => {
  if (clicked == true) {
    clicked = false;
    n.href = "style2.css";
    sun.style.display = "none";
    car.src = "./images/index/style2/car.svg";
    theme.innerHTML = "serene";
    Top.display = "block";
  } else {
    clicked = true;
    n.href = "style.css";
    sun.style.display = "flex";
    car.src = "./images/index/style/car.svg";
    theme.innerHTML = "classic";
    Top.display = "none";
  }
});
