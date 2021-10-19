window.addEventListener('load', () => {
    console.log("ready");

    const canvas = document.querySelector("#draw_canvas");
    const ctx = canvas.getContext("2d");

    //Resize
    canvas.height = 500;
    canvas.width = 500;
    canvas.getElementsByClassName.height = "100%";
    canvas.getElementsByClassName.width = "100%";

    let drawing = false;

    function startPosition(){
        drawing = true;
        ctx.beginPath();
    }

    function draw(e){
        if(!drawing) return;

        ctx.lineWidth = 40;
        ctx.lineCap = "round";

        
        if(e.type=="touchmove"){
            var touch = e.touches[0];
            ctx.lineTo(touch.clientX,touch.clientY-90);
            ctx.stroke();
            ctx.beginPath();
            ctx.lineTo(touch.clientX,touch.clientY-90);
        }
        else{
            var obj=canvas;
            var top = 0;
            var left = 0;
            while (obj) {
                top += obj.offsetTop;
                left += obj.offsetLeft;
                obj = obj.offsetParent;
            }
            const bounds = canvas.getBoundingClientRect();
            var mouseX = e.clientX - left + window.pageXOffset;
            var mouseY = e.clientY - top + window.pageYOffset;
            mouseX = (mouseX / bounds.width) * canvas.width;
            mouseY = (mouseY / bounds.height) * canvas.height;
            ctx.lineTo(mouseX, mouseY);
            ctx.stroke();
            ctx.beginPath();
            ctx.lineTo(mouseX,mouseY);
        }
        
    }

    function endPosition(){
        drawing = false;
    }

    function out(){
        drawing = false;
    }

    //EvenListeners
    canvas.addEventListener("mousedown", startPosition);
    canvas.addEventListener("mouseup", endPosition);
    canvas.addEventListener("mousemove", draw);
    canvas.addEventListener("mouseout", out);

    canvas.addEventListener("touchstart", startPosition);
    canvas.addEventListener("touchend", endPosition);
    canvas.addEventListener("touchmove", draw);



    document.getElementById("add").onclick = function(){ return process(0) };
    document.getElementById("predict").onclick = function(){ return process(1) };
    document.getElementById("del").onclick = function(){ return process(2) };
    document.getElementById("train").onclick = function(){ return process(3) };

    xhr = new XMLHttpRequest()
    function process(n){
        canvas_img = ctx.getImageData(0, 0, canvas.height, canvas.width);
        img_data = canvas_img.data;

        //Proces data when Add is clicked
        if(n==0 || n==1){
            img_pixels=[];
            for(i=3; i<img_data.length; i+=4){
                img_pixels.push(img_data[i])
            }

            for(i=0; i<img_pixels.length; i++){
                if(img_pixels[i] > 0){
                    str=JSON.stringify(img_pixels);
                    break;
                }
                if(i==img_pixels.length-1){
                    alert("Vacío");
                    n=100;
                }
            }
        }

        xhr.open("POST", "/");
        xhr.setRequestHeader("Content-Type", "text/plain");
        if(n==0){
            xhr.send(str + "/a");
        }
        else if (n==1){
            xhr.send(str + "/p");    
        }
        else if (n==2){
            xhr.send("/d");
        }
        else if (n==3){
            ground=document.getElementById("ground").value;
            document.getElementById("ground").value="";
            if(ground==""){
                alert("Indicar el número a entrenar")
            }
            else{
                xhr.send(JSON.stringify(ground) + "/t");
            }
        }

        xhr.onreadystatechange = function() {
            while(xhr.status != 200);
            location.reload();
        }

        //tests
 //       console.log(img_pixels);
  //      console.log(str);
    }
});