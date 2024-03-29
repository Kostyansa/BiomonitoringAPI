function generate() {
  const img = document.getElementById( 'imagePlaceHolder' );
  img.src = 'envatopreloader.gif';
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

function select_from_table(){

  const id = document.getElementById('id_data').value
  let sql_table = document.getElementById('sql_table')
  var invisible_row = document.getElementById('invisible_row')
  sql_table.innerHTML = "<tbody id='parent_table'> \
                          <tr> \
                            <td>id</td> \
                            <td>Название изображения</td> \
                            <td>Результаты анализа</td> \
                            </tr> \
                        </tbody> \
                        <div id='invisible_row' hidden='true'></div>"
  if (id == ""){
    sql_table.removeAttribute('hidden')
    var parent_table = document.getElementById('parent_table')
    axios.get('/bioobject/')
      .then(function (res) {
      console.log(res.data)
      for (i = 0; i < res.data.length; i++){
        var data = JSON.parse(res.data[i])
        elem = document.createElement('tr')
        elem.innerHTML = "<td>" + data.uuid + "</td> \
          <td>" + data.original + "</td> \
          <td>" + "Некроз:" + data.analysis.necrosis_percentage + "%  " +
			"Гниль:" + data.analysis.rot_percentage + "%  " +
			"Белая плесень:" + data.analysis.white_mold_percentage + "%  " +
			"Зеленая плесень:" + data.analysis.green_mold_percentage + "%  " +
			"</td>"
      parent_table.appendChild(elem)
      }
      })
  }
  else{
    axios.get('/bioobject/get?id=' + id)
      .then(function (res) {
        sql_table.setAttribute('hidden', 'true')
	let data = JSON.parse(res.data) 
        green_mold_percentage = document.getElementById( 'green_mold_percentage' );
        green_mold_percentage.innerHTML = data.analysis.green_mold_percentage + '%';
      
        white_mold_percentage = document.getElementById( 'white_mold_percentage' );
        white_mold_percentage.innerHTML = data.analysis.white_mold_percentage + '%';
      
        rot_percentage = document.getElementById( 'rot_percentage' );
        rot_percentage.innerHTML = data.analysis.rot_percentage + '%';
      
        necrosis_percentage = document.getElementById( 'necrosis_percentage' );
        necrosis_percentage.innerHTML = data.analysis.necrosis_percentage + '%';

		    const img = document.getElementById( 'imagePlaceHolder' );
    		    img.src = data.analysis.path_to_picture;
      })
    

  }
}
