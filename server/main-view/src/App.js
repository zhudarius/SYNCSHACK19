import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios';

class App extends Component {
  constructor() {
    super();

    this.state = {
      displayData: [],
      loading: true
    }
  }


  componentDidMount() {
    console.log("test");
    axios.get(`asdf`)
      .then(res => {
        const displayData = res.data;
        this.setState({ displayData });

        this.setState({ loading: false });
        console.log("Success get data");
        console.log(displayData);
      })
      .catch(err => {
        const displayData = err;
        this.setState({ displayData: "Oops, something went wrong requesting data!" });
        this.setState({ loading: false });
        console.log("Fail get data");
        console.log(displayData.toString());

      })
  }

  render() {
    return this.state.loading === true ?
      <div>Loading...</div>
      :
      <div>
        <div>
          <ul>
            {this.state.displayData
              /* {this.state.displayData.map(d => {
              return <li>{d}</li>
            })} */}
          </ul>
        </div>
      </div>

  }
}

export default App;
