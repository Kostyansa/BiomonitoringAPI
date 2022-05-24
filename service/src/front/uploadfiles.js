document.getElementById('buttonid').addEventListener('click', generate);

function generate() {
  let file = document.getElementById("fileid").files[0];
  let formData = new FormData();
  formData.append("file",file,file.name)
  console.log(formData)
  axios.post('http://127.0.0.1:5000/analyse', formData, {
    headers: {
      'content-Type': 'multipart/form-data'
    }
}).then(function (res) 
		 {
              output.className = 'container';
		   const img = document.createElement( 'img' );
		   imgBlob = btoa(res.data);
		   console.log(imgBlob);
		   const url = URL.createObjectURL(imgBlob); 
    		   img.src = url;
              output.appendChild(img);
            })
            .catch(function (err) {
              output.className = 'container text-danger';
              output.innerHTML = err.message;
            });
}