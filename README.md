RUNTIME PLANTA BAIXA DA FÁBRICA EM TEMPO REAL
(Utiliza a informação do sistema da fábrica e transforma num monitoramento visual)

- API backend que consulta dados de uma fonte API WEB e junta com outra fonte utilizando web scraping com Python Selenium (dados de uma página), essa coleta ocorre num loop a cada 10 segundos e escreve num arquivo JSON numa pasta de rede
- O servidor python começa a rodar no host 8000 e lê essa API JSON na pasta de rede e escreve num endpoint
- O HTML junto com o Javascript faz um get dos dados do endpoint dentro de um loop, e passa por cada DIV e compara com cada objeto do JSON para mudar as cores de acordo com as informações contidas, assim obtendo a informação se o posto de trabalho está produzindo ou se está parado

![image](https://github.com/danielss0n/Runtime-Caldeiraria/assets/82897131/fbe8ee95-a8af-4087-828d-9717a46a1a08)

![image](https://github.com/user-attachments/assets/30daae67-a934-4d0e-a3b7-c2f3cff0b938)


## Javascript que passa pelo JSON e o HTML:
```javascript
laborDivs.forEach(div => {
  const matchingObject = groupedJson.find(obj => obj.Workstation === div.id);

  if (matchingObject) {
      // Remove all P elements
      var P = div.querySelectorAll('p');
      P.forEach(function(eventElement) {
          eventElement.parentNode.removeChild(eventElement);
      });

      // Text of workstation name
      const workstationNameTextElement = document.createElement('p');
      workstationNameTextElement.id = `${matchingObject.Workstation}WorsktationName`;
      workstationNameTextElement.className = `worsktation-name`;
      workstationNameTextElement.textContent = matchingObject.Workstation;
      workstationNameTextElement.style.color = getTextColor(matchingObject.AreaEventColor);

      div.appendChild(workstationNameTextElement);
  
      // Make the event element, ex: OPERANDO (3)
      const eventsCountArray = countEvents(matchingObject.Events)
      for (let key in eventsCountArray) {
          const countValue = eventsCountArray[key];

          var string = `${key}`;
          if (countValue > 1) {
              string = `${key} (${countValue})`;
          } 

          const EVENT = document.createElement('p');
          EVENT.id = `${event}`;
          EVENT.className = `event`;
          EVENT.textContent = string;
          EVENT.style.color = getTextColor(matchingObject.AreaEventColor);

          div.appendChild(EVENT);
      }

      // Count how many same events have in one workstation
      function countEvents(events) {
          const count = {};
          events.forEach(value => {
              if (count[value]) {
                  count[value]++;
              } else {
                  count[value] = 1;
              }
          });
          return count;
      }
      
      // Background color style
      div.style.backgroundColor = matchingObject.AreaEventColor;
      switch(matchingObject.AreaEventColor) {
          case "green": div.style.backgroundColor = "rgb(0, 186, 16)"; break
          case "red": div.style.backgroundColor = "rgb(255, 0, 0)"; break
          case "yellow": div.style.backgroundColor = "rgb(240, 212, 0)"; break
      }

      // Font color style
      function getTextColor(event) {
          switch(event) {
              case "red": return "white"; 
              case "green": return "white";
              case "yellow": return "white";
          }  
      }
  }
})
} 
} catch (error) {
console.log(error)
}
