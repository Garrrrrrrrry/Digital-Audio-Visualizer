let input = document.getElementById('searchbar');

input.addEventListener("keypress", (e) =>
{
  if(e.key == "Enter")
  {
    var input_value = input.value;
    console.log(input_value);
    sendToPy(input_value);
  }
})

function sendToPy(input) {
  $.ajax
    (
      {
        type: "POST",
        url: '/analyzer.py',
        data: { param: input },
        success: returnData
      }
    );
}

//returndata function not reached
function returnData(response) {
  console.log("reached1")
  console.log(response)
}

console.log("reached2")