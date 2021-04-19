import React, {useState, useEffect} from "react";
import './ProcessListStyle.css';

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
        <td className="PTableCell"><img src={`data:image/png;base64,${process.icon}`}  /></td>
        <td className="PTableCell">{process.pid
        .map((pid) => <span className="Pid">{pid}</span>)
        .reduce((prev,curr) => [prev, ', ', curr])}</td>
        <td className="PTableCell">{process.application}</td>
    </tr>)

    return  <div className="Process-Table">
        <table className="PTable">
            <thead>
                <tr>
                    <th className="icon">Icon</th>
                    <th className="pid">PIDs</th>
                    <th className="application">Application Name</th>
                </tr>
            </thead>
            <tbody>{listItems()}</tbody>
        </table>
    </div>
    
    
}
