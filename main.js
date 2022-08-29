
let input = document.getElementById('searchbar');

input.addEventListener("keypress", (e) =>
{
  if(e.key == "Enter")
  {
    var name = input.value;
    console.log(name);

      $.ajax ({
        url: '/analyzer',
        data: name,
        type: "POST",
        success: function(response) {
          console.log("Success: ", response);
        },
        error: function(error) {
          console.log("Error: ", error);
        }
      })
  }
})

//PROBLEM: outputs source code instead of actual output of code

/*function returnData(response) {
  console.log("reached1")
  console.log(response)
}*/
console.log("reached2");