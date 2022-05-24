document.getElementById('buttonid').addEventListener('click', generate);

function generate() {
  let file = document.getElementById("fileid").files[0];
  let formData = new FormData();
  formData.append("file",file,file.name)
  console.log(formData)
  axios.post('/analyse/', formData, {
    headers: {
      'content-Type': 'multipart/form-data'
    }
}).then(function (res) 
		 {
              output.className = 'container';
      green_mold_percentage = document.getElementById( 'green_mold_percentage' );
      green_mold_percentage.innerHTML = res.data.green_mold_percentage + '%';
      
      white_mold_percentage = document.getElementById( 'white_mold_percentage' );
      white_mold_percentage.innerHTML = res.data.white_mold_percentage + '%';
      
      rot_percentage = document.getElementById( 'rot_percentage' );
      rot_percentage.innerHTML = res.data.rot_percentage + '%';
      
      necrosis_percentage = document.getElementById( 'necrosis_percentage' );
      necrosis_percentage.innerHTML = res.data.necrosis_percentage + '%';

		   const img = document.getElementById( 'imagePlaceHolder' );
    		   img.src = res.data.path_to_picture;
              //output.appendChild(img);
            })
            .catch(function (err) {
              output.className = 'container text-danger';
              output.innerHTML = err.message;
            });
}
