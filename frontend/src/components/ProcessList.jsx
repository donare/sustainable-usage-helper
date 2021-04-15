import React, {useState, useEffect} from "react";

export default function ProcessList(props) {
    const [data, setData] = useState([]);
    const [isLoading, setLoading] = useState(true);

    const getData = async () => {
            const res = await fetch("http://localhost:8000/running_processes")
            const data = await res.json();
            setData(data)
        }   
  
    useEffect(() => {
        if (isLoading) {
            getData()
        }
        setLoading(false)
    }, [isLoading]);    

    if (isLoading) {
        return <p>Json not loaded yet</p>
    } 
    
    const listItems = () => data.map((process) => 
    <tr key = {process.pid}>
        <td><img src={`data:image/png;base64,${process.icon}`}  /></td>
        <td>{process.pid}</td>
        <td>{process.application}</td>
    </tr>)

    return  <div className="Process-Table">
        <table>
            <thead>
                <tr>
                    <td>Icon</td>
                    <td>PID</td>
                    <td>Application Name</td>
                </tr>
            </thead>
            <tbody>{listItems()}</tbody>
        </table>
    </div>
    
    
}
