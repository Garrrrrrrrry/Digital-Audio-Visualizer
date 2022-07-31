let input = "hi1";//document.getElementById('searchbar').value;

function sendToPy(input) {
  $.ajax
    (
      {
        type: "POST",
        url: "/analyzer.py",
        data: { param: input },
        success: returnData
      }
    );
}

function returnData(response) {
  console.log("test")
  console.log("output" + response)
}

console.log("reached")