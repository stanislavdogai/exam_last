async function makeRequest(url, method) {
    let response = await fetch(url, method);
    if (response.ok) {
        return await response.json();
    } else {
        let error = new Error(response.statusText);
        error.response = response;
        err_response = await response.json()
        return err_response
    }
}

let public = async function(event){
    let url = event.target.dataset.publicId
    let data = await makeRequest(url,  {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        })
    if(data){
        let p = document.getElementById('moderated-text');
        p.innerText = data.message;
    }
}

let cancel = async function(event){
    let url = event.target.dataset.cancelId
    console.log(url)
    let data = await makeRequest(url,  {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        })
    console.log(data)
    if(data){
        let p = document.getElementById('moderated-text');
        p.innerText = data.message;
    }
}