

window.onload = function(){
  const constr = {
    video: true,
    audio: true
  };

  let blob = new Blob();

  let Save = document.getElementById('btnSave');

  navigator.mediaDevices.getUserMedia(constr)
    .then(function(mediaStream){
        let video = document.querySelector('video');
        video.srcObject = mediaStream;

        video.onloadedmetadata = function(ev){
            video.play();
        };

        //listners for a vid recording
        let start = document.getElementById('btnStart');
        let stop = document.getElementById('btnStop');
        let status = document.getElementById('status');
        let mediaRecorder = new MediaRecorder(mediaStream);
        let vidSave = document.getElementById('vidSave');
        let chunks = [];

        start.addEventListener('click', (e)=>{
            debugger;
            status.innerText = 'Status: start recording';
            mediaRecorder.start();
            console.log(mediaRecorder.state);
        });

        stop.addEventListener('click', (e) =>{
            debugger;
            status.innerText = 'Status: stop recording';
            mediaRecorder.stop();
            console.log(mediaRecorder.state);
        });

        mediaRecorder.ondataavailable = function (e) {
            chunks.push(e.data);
        };

        mediaRecorder.onstop = (e) => {
            blob = new Blob(chunks, { type: 'video/mp4;'});
            chunks = [];
            let videoUrl = window.URL.createObjectURL(blob);
            vidSave.src = videoUrl;
        }

    }).catch(function(err){
      console.log(err.name, err.message);
    })


    Save.addEventListener('click', (e) => {
        debugger
        status.innerText = 'Status: video save';
        let url = 'http://127.0.0.1:8000/video/save';
        let headers = new Headers({'Accept': 'application/json'});
        let data = new FormData();
        data.append('video', blob);
        data.append('csrfmiddlewaretoken', document.getElementsByName('csrfmiddlewaretoken')[0].value)
        let req = new Request(url, {
            method: 'POST',
            headers: headers,
            mode: 'no-cors',
            body: data
        })

        fetch(req).then((response)=>{
            console.log(response.message)
            location.reload()
        }).catch((err) => {
            console.log(err.message)
        });
    });



};
