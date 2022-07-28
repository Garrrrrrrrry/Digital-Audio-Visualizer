let input = document.getElementById('searchbar').value;

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

await function returnData(response) {
  console.log(response)
}