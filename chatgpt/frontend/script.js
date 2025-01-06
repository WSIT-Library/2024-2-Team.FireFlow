let userMessages = [];
let assistantMessages = [];

async function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value;
  
    // 사용자 메시지 출력
    const userBubble = document.createElement('div');
    userBubble.className = 'chat-bubble user-bubble';
    userBubble.textContent = message;
    document.getElementById('fortuneResponse').appendChild(userBubble);
  
    // 입력된 메시지 리스트에 추가
    userMessages.push(message);

    
    messageInput.value = ''; // 입력 필드 초기화
  
    try {
      const response = await fetch('http://localhost:3000/Tell', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          userMessages: userMessages,
          assistantMessages: assistantMessages,
        })
      });
  
      if (!response.ok) {
        throw new Error('Request failed with status '+ response.status);
    }

    const data = await response.json();

    assistantMessages.push(data.assistant);
    console.log('Parsed Response:', data);
    console.log("assistantmessage:",data.assistantMessages);


    //채팅 말풍선에 챗GPT 응답 출력
    const botBubble = document.createElement('div');//div생성
    botBubble.className = 'chat-bubble bot-bubble';//id값
    botBubble.textContent = data.assistant;//데이터 넣기
    document.getElementById('fortuneResponse').appendChild(botBubble);


} catch (error) {
    console.error('Error:', error);
}
}