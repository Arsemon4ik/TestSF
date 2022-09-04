import React, {useEffect} from 'react';

function App() {

  const getReformatData = async () => {
    const response = await fetch ("http://127.0.0.1:8000/visited_links/")
    console.log(await response.json())
  }

  const sendRowData = async () =>{
    const url = 'http://127.0.0.1:8000/visited_links/';
    const data = { links: [
        "https://ya.ru",
        "https://ya.ru?q=123",
        "funbox.ru",
        "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor"
      ]};

    try {
      const response = await fetch(url, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
          'Content-Type': 'application/json'
        }
      });
      const json = await response.json();
      console.log('Успех:', JSON.stringify(json));
    } catch (error) {
      console.error('Ошибка:', error);
    }
  }
  // useEffect(()=>{
  //   getReformatData()
  // })
  return (
    <div className="App">
      <h1>It's works!</h1>
      <button style={{width: '150px'}} onClick={() => sendRowData()}>Отправить данные</button>
      <button style={{width: '150px'}} onClick={() => getReformatData()}>Получить данные</button>
    </div>
  );
}

export default App;
