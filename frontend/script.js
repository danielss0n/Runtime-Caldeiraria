async function updateDivsWithBackendData() {
    try {
        const response = await fetch('http://ip:host')
        
        if (response.ok) {
            const jsonData = await response.json();
            const laborDivs = document.querySelectorAll('div');
        
            // Create new json with array of events of the unified workstation
            const workstationMap = {};
            jsonData.forEach(obj => {
                const workstation = obj.Workstation;
                if (!workstationMap[workstation]) {
                    workstationMap[workstation] = {
                        Events: [],
                        AreaEventColor: obj.AreaEventColor 
                    };
                }
                workstationMap[workstation].Events.push(obj.Event);
            });

            // Extract the necessary data
            const groupedJson = Object.entries(workstationMap).map(([workstation, data]) => {
                return {
                    Workstation: workstation,
                    Events: data.Events,
                    AreaEventColor: data.AreaEventColor
                }
            });

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
}
updateDivsWithBackendData()
setInterval(updateDivsWithBackendData, 10000)