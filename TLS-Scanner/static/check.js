
async function scanURL(e)
{   
    alert(e)
    const body = {'url':e}
    console.log(body)
    await axios.get('/check?url='+e)
    .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
    // var newDiv= document.createElement("div")
    // newDiv.id = "data"
    // newDiv.innerHTML(data)
    // document.body.appendChild(myDiv);   
}   