


async function llmResponse(historyList) {
  
  try {
    const response = await fetch("http://127.0.0.1:8000/rag_llm", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ "messages": historyList.length>=3? historyList.slice(-3): historyList }),
    });

    if (!response.ok) {
      h=localStorage.getItem("chatHistory")
      history_list=JSON.parse(h)
      history_list.pop()
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json(); 
    
    let messageContainer=document.getElementById('messageContainer')
    let left_container=document.createElement("div")
    left_container.classList.add('d-flex')
    left_container.classList.add('justify-content-start')
    h=localStorage.getItem("chatHistory")
    history_list=JSON.parse(h)
    history_list.push({"role":"assistant", "content":data})
    localStorage.setItem("chatHistory",JSON.stringify(history_list))
    messageContainer.append(left_container)
    left_container.innerHTML='<span><img src="chatbot_logo.png" height="35" class="p-1"> </span>'
    let left_div=document.createElement("div")
    left_div.className='left_message'
    
    left_div.innerHTML=data
    left_container.append(left_div)

    return data;
  } catch (error) {
    console.error("Fetch error:", error);
  }
}

function sendQuery(){

  debugger

  let messageBox=document.getElementById('messageBox')
  let messageContainer=document.getElementById('messageContainer')
  
  let right_div=document.createElement("div")
  right_div.className='right_message'
  right_div.innerHTML=messageBox.value

  h=localStorage.getItem("chatHistory")
  if (h){

    history_list=JSON.parse(h)
    history_list.push({"role":"user", "content":messageBox.value})
    localStorage.setItem("chatHistory",JSON.stringify(history_list))
    
  }
  else{
    
  
    localStorage.setItem("chatHistory",JSON.stringify([{"role":"user", "content":messageBox.value}]))

  }
  

    

  response=llmResponse(JSON.parse(localStorage.getItem('chatHistory')))
  messageContainer.append(right_div)
  messageBox.value=''
  
  



}


function handleKeyDown(event) {
  if (event.key === "Enter") {
      sendQuery();
  }
}



function loadHistory(){
  debugger
  let messageContainer=document.getElementById('messageContainer')

  h=localStorage.getItem("chatHistory")
  history_list=JSON.parse(h)
  if(h){

    for (message of history_list){
      if(message['role']=='user'){
        let right_div=document.createElement("div")
        right_div.className='right_message'
        right_div.innerHTML=message['content']
        messageContainer.append(right_div)

      }
      else{
        if(message['role']=='assistant'){
          let left_container=document.createElement("div")
      left_container.classList.add('d-flex')
      left_container.classList.add('justify-content-start')
      messageContainer.append(left_container)
      left_container.innerHTML='<span><img src="chatbot_logo.png" height="35" class="p-1"> </span>'
      let left_div=document.createElement("div")
      left_div.className='left_message'
      left_div.innerHTML=message['content']
      left_container.append(left_div)
        }
      }
    }
  }

}



function deleteHistory(){
  let messageContainer=document.getElementById('messageContainer')
  initialElememnt=document.getElementById("initial")
  messageContainer.innerHTML=initialElememnt.outerHTML
  localStorage.removeItem("chatHistory")
}






  
