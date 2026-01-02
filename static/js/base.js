//Registration and initiate POST request
const regForm=document.getElementById('registerForm')
if(regForm){
	regForm.addEventListener('submit', async function(event){
		event.preventDefault();
		
		const form=event.target;
		const formData=new FormData(form);
		const data=Object.fromEntries(formData.entries())
		
		if(data.password !== data.password2){
			alert("Passwords dont match")
			return
		}
		const payload={
			email:data.email,
			username:data.username,
			first_name:data.firstname,
			last_name:data.lastname,
			role:data.role,
			password:data.password,
			is_active:true,
			phone_number:data.phone
		};
		console.log(JSON.stringify(payload));
		try{
			const response=await fetch('/auth/create',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
			if(response.ok){
				window.location.href='/auth/login'
			}
			else{
				const errordata=response.json();
				alert(`error:${errordata.message}`)
			}
		}
		catch(error){
			console.error('error',error)
			alert('an error occurred, please try again')
			
		}
		
	});
}

const loginForm=document.getElementById('loginForm')
if (loginForm){
    loginForm.addEventListener('submit',async function(event){
        event.preventDefault();

        const form =event.target;
        const formData= new FormData(form);
        const payload=new URLSearchParams();
        for(const [key,value] of formData.entries()){
            payload.append(key,value)
        }
        console.log(payload.toString())
        try{
        const response= await fetch('/auth/token',{
            method:'POST',
            headers:{
                'Content-Type':'application/x-www-form-urlencoded'
            },
            body:payload.toString()

        });
        if(response.ok){
            const data= await response.json();
            logout();
            document.cookie=`access_token=${data.access_token}; path=/`
            console.log('cookie saved successfully')
            //console.log(data.access_token)
            //console.log(document.cookie)
            window.location.href="/todos/todo-page";
        }
        else{
            const errorData = await response.json();
            alert(`Error: ${errorData.detail}`);

        }
        }
        catch(error){
            console.log('error:',error);
            alert('an error occurred');
        }



    });
}

const addForm=document.getElementById('addForm');
if(addForm){
    addForm.addEventListener('submit',async function(event){
        event.preventDefault();
        const form=event.target;
        const formData=new FormData(form);
        const data=Object.fromEntries(formData.entries());

        console.log(typeof(data.priority));
        payload={
            title:data.title,
            description:data.description,
            priority:parseInt(data.priority),
            complete:data.complete
        }

       try{
            const response=await fetch('/todos/add-todo',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
            if(response.ok){
            console.log('write Successful');
            window.location.href='todo-page';
            }
       }
       catch(error){
        console.log('error:',error);
       }
    });
}


function logout(){
    console.log(document.cookie);
    const cookies=document.cookie.split(';');
    console.log(cookies);

    for(let i=0;i<cookies.length;i++){
        const cookie=cookies[i];
        console.log(cookie);

        const eqPos= cookie.indexOf('=');
        console.log(eqPos);

        name='';
        for(let j=0;j<eqPos;j++){
				name=name+cookie[j];
		}
		document.cookie=name+'=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/';


    }
}

const editForm=document.getElementById('editForm');
if(editForm){
    editForm.addEventListener('submit', async function(event){
        event.preventDefault();
        const form=event.target;
        const formData=new FormData(form);
        const data=Object.fromEntries(formData.entries());
        console.log(data);

        var url=window.location.pathname;
        lastSlash=url.lastIndexOf('/');
        var todo_id='';
        for(let i=lastSlash+1;i<url.length;i++){
            todo_id=todo_id+url[i];
        }
        console.log(typeof(todo_id));

        payload2={
            id:parseInt(todo_id),
            title:data.title,
            description:data.description,
            priority:parseInt(data.priority),
            complete:data.complete
        }
        try{
            const response=await fetch('/todos/update-todo',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload2)});
            if(response.ok){
            console.log('write Successful');
            window.location.href='/todos/todo-page';
            }
       }
       catch(error){
        console.log('error:',error);
       }
    });

    const deleteTodo=document.getElementById('deleteButton');
    if(deleteButton){
        deleteButton.addEventListener('click',async function(delevent){
            delevent.preventDefault();

            var url=window.location.pathname;
            lastSlash=url.lastIndexOf('/');
            var todo_id='';
            for(let i=lastSlash+1;i<url.length;i++){
                todo_id=todo_id+url[i];
            }
            console.log(todo_id);
            token=getCookie('access_token')

             try{
                const response=await fetch(`/todos/delete-todo/${todo_id}`,{method:'DELETE',headers:{'Authorization':`Bearer${token}`}});
                if(response.ok){
                    console.log('delete Successful');
                    window.location.href='/todos/todo-page';
                }
             }
             catch(error){
                console.log('error:',error);
             }
        });
    }

}

function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };
