import React from 'react';
import DatePicker from "react-datepicker";
import axios from 'axios';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useHistory,
  useParams
} from "react-router-dom";

import "react-datepicker/dist/react-datepicker.css";
import "bootstrap/dist/css/bootstrap.min.css";

class App extends React.Component {
	render() {
  	return (
    	<div className='container'>
        <Router>
        <Switch>
          <Route path="/query/:ntid" component={QueryForm} />
          <Route path="/reporter/:ntid" component={ReporterForm} />
          <Route path="/usertype/:ntid" component={UserType} />
          <Route path="/" component={LoginForm} />
        </Switch>
        </Router>
    	</div>
    );
  }	
}

class LoginForm extends React.Component {
  state = { name: '', password: '', show_error: false};

  handleSubmit = async (event) => {
    event.preventDefault();
    const resp = await axios.post('http://localhost:5000/login', {
      name : this.state.name,
      password : this.state.password
    });

    if (resp.data.auth) {
      this.setState({show_error: false})
      this.props.history.push(`/usertype/` + this.state.name)
    }
    else {
      this.setState({show_error: true})
      this.setState({ name: '', password: '' });
    }
  };

	render() {
  	return (
    	<form onSubmit={this.handleSubmit}>
        <span className="formtext"><p style={{'fontWeight':'bold','fontSize':'3vw'}}>Sign In</p></span>
        <label>NTID:</label>
    	  <input className='form-control'
          type="text" 
          value={this.state.name}
          onChange={event => this.setState({ name: event.target.value})}
          placeholder="NTID" 
          required 
        /> <br/>

        <label>Password:</label>
        <input className='form-control'
          type="password" 
          value={this.state.password}
          onChange={event => this.setState({ password: event.target.value})}
          placeholder="Password" 
          required 
        /> <br/>

        <button className='btn btn-primary'>Login</button>
        {this.state.show_error ? <div className='alert alert-danger'>User not found!</div>:null}
    	</form>
    );
  }
}

class UserType extends React.Component {
  render() { 
    let ntid = this.props.match.params.ntid;
    console.log(this.props);
    return(
      <div>
        <span className="headertext"><p style={{'fontWeight':'bold','fontSize':'3vw'}}>Select User Type</p></span>
        <button className='btn btn-primary' onClick={event => this.props.history.push('/reporter/' + ntid)}>Reporter</button> <br/><br/>
        <button className='btn btn-primary' onClick={event => this.props.history.push('/query/' + ntid)}>Query</button>
      </div>
    );
  }
}

class ReporterForm extends React.Component {
  state = { reporter: '', 
            metricName: '',
            database: 'NDW',
            schema: '',
            table: '',
            metricId: '',
            metricCol: '',
            excl_bulk: false,
            excl_resi: true,
            excl_courtesy: false,
            ned: true,
            cen: true,
            wes: true,
            divisionCol: '',
            regionCol: '',
            topGeoAgg: 'ENT',
            timeCol: '',
            timeDensity: 'D',
            startDate: '',
            endDate: ''
          };

  handleSubmit = async (event) => {
    let ntid = this.props.match.params.ntid;
    console.log(this.props);
    event.preventDefault();
    const resp = await axios.put('http://localhost:5000/report', {
      reporter: ntid, 
      metricName: this.state.metricName,
      database: this.state.database,
      schema: this.state.schema,
      table: this.state.table,
      metricId: this.state.metricId,
      metricCol: this.state.metricCol,
      exclusions: {'excl_bulk': this.state.excl_bulk, 
                  'excl_resi': this.state.excl_resi, 
                  'excl_courtesy': this.state.excl_courtesy},
      geos: {'ned': this.state.ned, 
            'cen': this.state.cen, 
            'wes': this.state.wes},
      divisionCol: this.state.divisionCol,
      regionCol: this.state.regionCol,
      topGeoAgg: this.state.topGeoAgg,
      timeCol: this.state.timeCol,
      timeDensity: this.state.timeDensity,
      dateRange: {'start_date':this.state.startDate, 'end_date':this.state.endDate}
    });

    this.setState({ reporter: '', 
            metricName: '',
            database: 'NDW',
            schema: '',
            table: '',
            metricId: '',
            metricCol: '',
            excl_bulk: false,
            excl_resi: true,
            excl_courtesy: false,
            ned: true,
            cen: true,
            wes: true,
            divisionCol: '',
            regionCol: '',
            topGeoAgg: 'ENT',
            timeCol: '',
            timeDensity: 'D',
            startDate: '',
            endDate: '' });
            
    this.props.history.push(`/usertype/` + ntid)
  
  };
    
  render() {
  	return (
    	<form onSubmit={this.handleSubmit}>
        <span className="formtext"><p style={{'fontWeight':'bold','fontSize':'3vw'}}>Add New Metric</p></span>
    	  <label>Metric Name*:</label>
        <input className='form-control' 
          type="text" 
          value={this.state.metricName}
          onChange={event => this.setState({ metricName: event.target.value})}
          placeholder="metric name" 
          required 
        /> <br/>
        
        <label>Database*:</label>
        <select className='form-control'
          value={this.state.database}
          onChange={event => this.setState({ database: event.target.value})}>
          <option value="NDW">NDW</option>
          <option value="MELD">MELD</option>
          required 
        </select> <br/>
        
        <label>Schema*:</label>
        <input className='form-control'
          type="text" 
          value={this.state.schema}
          onChange={event => this.setState({ schema: event.target.value})}
          placeholder="schema" 
          required 
        /> <br/>

        <label>Table*:</label>
        <input className='form-control'
          type="text" 
          value={this.state.table}
          onChange={event => this.setState({ table: event.target.value})}
          placeholder="table" 
          required 
        /> <br/>
        
        <label>Metric Id*:</label>
        <input className='form-control'
          type="text" 
          value={this.state.metricId}
          onChange={event => this.setState({ metricId: event.target.value})}
          placeholder="metric Id" 
          required 
        /> <br/>      
        <label>Metric Column*:</label>
        <input className='form-control'
          type="text" 
          value={this.state.metricCol}
          onChange={event => this.setState({ metricCol: event.target.value})}
          placeholder="metric column" 
          required 
        /> <br/>

        <label>Exclude Bulk?*:</label>&nbsp;
        <div style={{'marginLeft':'35px'}} className='form-check form-check-inline'>
          <input className='form-check-input'
          type="radio" 
          value="Yes"
          checked={this.state.excl_bulk === true}
          onChange={event => this.setState({ excl_bulk: true})}
          required 
          /> 
          <label className='form-check-label'>Yes</label> 
        </div>
        <div className='form-check form-check-inline'>
          <input className='form-check-input'
            type="radio" 
            value="No"
            checked={this.state.excl_bulk === false}
            onChange={event => this.setState({ excl_bulk: false})}
            required 
          /> 
          <label className='form-check-label'>No</label> 
        </div><br/>

        <label>Resi?*:</label>
        <div style={{'marginLeft':'101px'}} className='form-check form-check-inline'>
          <input className='form-check-input '
            type="radio" 
            value="Yes"
            checked={this.state.excl_resi === true}
            onChange={event => this.setState({ excl_resi: true})}
            required 
          /> 
          <label className='form-check-label'>Yes</label> 
        </div>
        <div className='form-check form-check-inline'>
          <input className='form-check-input'
            type="radio" 
            value="No"
            checked={this.state.excl_resi === false}
            onChange={event => this.setState({ excl_resi: false})}
            required 
          /> 
          <label className='form-check-label'>No</label>
        </div><br/>

        <label>Exclude Courtesy?*:</label>&nbsp;
        <div className='form-check form-check-inline'>
          <input className='form-check-input'
            type="radio" 
            value="Yes"
            checked={this.state.excl_courtesy === true}
            onChange={event => this.setState({ excl_courtesy: true})}
            required 
          /> 
          <label className='form-check-label'>Yes</label> 
        </div>
        <div className='form-check form-check-inline'>
          <input className='form-check-input'
            type="radio" 
            value="No"
            checked={this.state.excl_courtesy === false}
            onChange={event => this.setState({ excl_courtesy: false})}
            required 
        /> 
        <label className='form-check-label'>No</label>
        </div><br/><br/>
        
        <label>Divisions:</label>&nbsp;
        <div className='form-check form-check-inline'>
        <input className='form-check-input'
          type="checkbox" 
          value="NED"
          checked={this.state.ned === true}
          onChange={event => this.setState({ ned: event.target.checked})}
          /> 
          <label className='form-check-label'>NED</label>
        </div> 
        <div className='form-check form-check-inline'>
          <input className='form-check-input'
            type="checkbox" 
            value="CEN"
            checked={this.state.cen === true}
            onChange={event => this.setState({ cen: event.target.checked})}
          />
          <label className='form-check-label'>CEN</label>
        </div>
        <div className='form-check form-check-inline'>
          <input className='form-check-input'
            type="checkbox" 
            value="WES"
            checked={this.state.wes === true}
            onChange={event => this.setState({ wes: event.target.checked})}
          /> 
          <label className='form-check-label'>WES</label> 
        </div> <br/>

        <label>Division Column (If None, leave blank):</label>
        <input className='form-control' 
          type="text" 
          value={this.state.divisionCol}
          onChange={event => this.setState({ divisionCol: event.target.value})}
          placeholder="division column" 
        /> <br/>

        <label>Region Column (If None, leave blank):</label>
        <input className='form-control' 
          type="text" 
          value={this.state.regionCol}
          onChange={event => this.setState({ regionCol: event.target.value})}
          placeholder="region column" 
        /> <br/>

        <label>What is the top level geographic aggregation?*:</label>&nbsp;&nbsp;
        <div className='form-check form-check-inline'>
          <input className='form-check-input'
            type="radio" 
            value="Enterprise"
            checked={this.state.topGeoAgg === 'ENT'}
            onChange={event => this.setState({ topGeoAgg: 'ENT'})}
            required 
        /> 
        <label className='form-check-label'>Enterprise</label>
        </div>
        <div className='form-check form-check-inline'>
          <input className='form-check-input'
            type="radio" 
            value="NED"
            checked={this.state.topGeoAgg === 'NED'}
            onChange={event => this.setState({ topGeoAgg: 'NED'})}
            required 
          /> 
          <label className='form-check-label'>NED</label> 
        </div>
        <div className='form-check form-check-inline'>
          <input className='form-check-input'
            type="radio" 
            value="CEN"
            checked={this.state.topGeoAgg === 'CEN'}
            onChange={event => this.setState({ topGeoAgg: 'CEN'})}
            required 
        /> 
        <label className='form-check-label'>CEN</label>
        </div>
        <div className='form-check form-check-inline'>
          <input className='form-check-input'
            type="radio" 
            value="WES"
            checked={this.state.topGeoAgg === 'WES'}
            onChange={event => this.setState({ topGeoAgg: 'WES'})}
            required 
        /> 
        <label className='form-check-label'>WES</label>
        </div>
        <div className='form-check form-check-inline'>
          <input className='form-check-input'
            type="radio" 
            value="Other"
            checked={this.state.topGeoAgg === 'Other'}
            onChange={event => this.setState({ topGeoAgg: 'Other'})}
            required 
        /> 
        <label className='form-check-label'>Other</label>
        </div>
        <br/><br/>

        <label>Time Column*:</label>
        <input className='form-control'
          type="text" 
          value={this.state.timeCol}
          onChange={event => this.setState({ timeCol: event.target.value})}
          placeholder="time column" 
          required 
        /><br/>
        <label>Time Granularity*:</label>
        <select 
          value={this.state.timeDensity}
          onChange={event => this.setState({ timeDensity: event.target.value})}>
          <option value="D">Daily</option>
          <option value="W">Weekly</option>
          <option value="M">Monthly</option>
          <option value="Y">Yearly</option>
          <option value="DW">Day of Week</option>
          required 
        </select> <br/><br/>

        <label>Start Date*:</label>&nbsp;&nbsp;
        <DatePicker 
          selected={this.state.startDate}
          onChange={date => this.setState({ startDate: date})} /><br/>

        <label>End Date*:</label>&nbsp;&nbsp;&nbsp;&nbsp;
        <DatePicker 
          selected={this.state.endDate}
          onChange={date => this.setState({ endDate: date})} /><br/><br/>

        <button className='btn btn-primary'>Submit</button>
    	</form>
    );
  }
}

class QueryForm extends React.Component {
  state = { metricName1: '',
            table1: '',
            metricName2: '',
            table2: '',
            show_error: false
          };
  

  handleSubmit = async (event) => {
    event.preventDefault();
    const resp = await axios.post('http://localhost:5000/query', {
      metricName1 : this.state.metricName1,
      table1 : this.state.table1,
      metricName2 : this.state.metricName2,
      table2 : this.state.table2
    });

    if (resp.data.status) {
      this.setState({show_error: false})
      window.Bokeh.embed.embed_item(resp.data.plot, 'plot')
    }
    else {
      this.setState({ metricName1: '',
      table1: '',
      metricName2: '',
      table2: '',
      show_error: true});
    }

    console.log(resp)
  
  };
    
  render() {
  	return (
      <div>
    	  <form onSubmit={this.handleSubmit}>
        <span className="formtext"><p style={{'fontWeight':'bold','fontSize':'3vw'}}>Query Metrics</p></span>
        <div className='row'>
          <div className='metricInput col'> <b>Metric 1</b> <br/>
            <label>Metric Name*:</label>
            <input className='form-control'
              type="text" 
              value={this.state.metricName1}
              onChange={event => this.setState({ metricName1: event.target.value})}
              placeholder="metric name" 
              required 
            /> <br/>

            <label>Table*:</label>
            <input className='form-control'
              type="text" 
              value={this.state.table1}
              onChange={event => this.setState({ table1: event.target.value})}
              placeholder="table" 
              required 
            /> 
          </div>
          <div className='metricInput col'> <b>Metric 2</b> <br/>
            <label>Metric Name*:</label>
            <input className='form-control'
              type="text" 
              value={this.state.metricName2}
              onChange={event => this.setState({ metricName2: event.target.value})}
              placeholder="metric name" 
              required 
            /> <br/>

            <label>Table*:</label>
            <input className='form-control'
              type="text" 
              value={this.state.table2}
              onChange={event => this.setState({ table2: event.target.value})}
              placeholder="table" 
              required 
            /> 
          </div>
        </div> <br/>
        
          <button className='btn btn-primary'>Query</button>
          {this.state.show_error ? <p>Metric not defined!</p>:null}
    	  </form>

        <div id='plot' className='bk-root'> 
        </div>
      </div>
    );
  }
}

export default App;
