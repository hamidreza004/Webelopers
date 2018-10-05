var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab

function showTab(n) {
  // This function will display the specified tab of the form ...
  var x = document.getElementsByClassName("tab");
  x[n].style.display = "block";
  // ... and fix the Previous/Next buttons:
  if (n == 0) {
    document.getElementById("prevBtn").style.display = "none";
  } else {
    document.getElementById("prevBtn").style.display = "inline";
  }
  if (n == (x.length - 1)) {
    document.getElementById("nextBtn").innerHTML = "درخواست آموزش";
  } else {
    document.getElementById("nextBtn").innerHTML = "بعدی";
  }
  if(n==2 || n==3 ){
      var a =document.getElementById("type");
      var selectedValue = a.options[a.selectedIndex].value;
      if(selectedValue == "2"){
        document.getElementById("location").style.display = "none";
        document.getElementById("loc").id="notchecked";
        document.getElementById("cache").style.display = "none";
      }
  }
  // ... and run a function that displays the correct step indicator:
  fixStepIndicator(n)
}

function nextPrev(n) {
  // This function will figure out which tab to display
  var x = document.getElementsByClassName("tab");
  // Exit the function if any field in the current tab is invalid:
  if (n == 1 && (!validateForm())) return false;
  // Hide the current tab:
  x[currentTab].style.display = "none";
  // Increase or decrease the current tab by 1:
  currentTab = currentTab + n;
  // if you have reached the end of the form... :
  if (currentTab >= x.length) {
    //...the form gets submitted:
    document.getElementById("regForm").submit();
    return false;
  }
  // Otherwise, display the correct tab:
  showTab(currentTab);
}

function validateForm() {
  // This function deals with validation of the form fields
  var x, y, i, valid = true, final=false;
  x = document.getElementsByClassName("tab");
  y = x[currentTab].getElementsByTagName("input");
  // A loop that checks every input field in the current tab:
  for (i = 0; i < y.length; i++) {
    // If a field is empty...
    if (y[i].value == "" && y[i].id !== 'notchecked') {
      // add an "invalid" class to the field:
      y[i].className += " invalid";
      // and set the current valid status to false:
      valid = false;
    }
  }
  // This function deals with validation of the form fields
  var a, b, j;
  a = document.getElementsByClassName("tab");
  b = x[currentTab].getElementsByTagName("select");
  // A loop that checks every input field in the current tab:
  for (j = 0; j < b.length; j++) {
    var selectedValue = b[j].value;
    // If a field is empty...
    if (selectedValue == "null") {
      // add an "invalid" class to the field:
      b[j].className += " invalid";
      // and set the current valid status to false:
      valid = false;
    }
  }
  // If the valid status is true, mark the step as finished and valid:
  if (valid && radio() && confirm() && time()) {
    var final=true;
    document.getElementsByClassName("step")[currentTab].className += " finish";
  }
  return final; // return the valid status
}
function confirm() {
  // This function deals with validation of the form fields
  var x, y, i, valid = true;
  x = document.getElementsByClassName("tab");
  y = x[currentTab].getElementsByTagName("input");
  // A loop that checks every input field in the current tab:
  for (i = 0; i < y.length; i++) {
    // If a field is empty...
   if (y[i].id == 'confirm'){
        if (y[i].checked == false) {
          // add an "invalid" class to the field:
          alert("در صورت عد قبول قوانین، امکان درخواست وجود ندارد.");
          y[i].focus();
          // and set the current valid status to false:
          valid = false;
        }
   }
  }
  return valid; // return the valid status
}
function time() {
  // This function deals with validation of the form fields
  var x, y, i,v, valid =true;
  x = document.getElementsByClassName("tab");
  y = x[currentTab].getElementsByTagName("input");
  // A loop that checks every input field in the current tab:
  for (i = 0; i < y.length; i++) {
    // If a field is empty...
   if (y[i].id == 'time'){
        if (y[i].checked == true) {
          return true;
        }
        valid = false;
   }
  }
  if (valid == false){
      alert("حداقل باید یکی از زمان‌ها را انتخاب کنید.");
  }
  return valid; // return the valid status
}
function radio() {
  // This function deals with validation of the form fields
  var x, y, i,v, valid =true;
  x = document.getElementsByClassName("tab");
  y = x[currentTab].getElementsByTagName("input");
  // A loop that checks every input field in the current tab:
  for (i = 0; i < y.length; i++) {
    // If a field is empty...
   if (y[i].id == 'radio1'){
        if (y[i].checked == true) {
          return true;
        }
        valid = false;
   }
  }
  if (valid == false){
      alert("باید یکی از گزینه‌ها را انتخاب کنید.");
  }
  return valid; // return the valid status
}


function fixStepIndicator(n) {
  // This function removes the "active" class of all steps...
  var i, x = document.getElementsByClassName("step");
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace("active", "");
  }
  //... and adds the "active" class to the current step:
  x[n].className += " active";
}