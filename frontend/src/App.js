import React, { useState, useEffect } from 'react';
// import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import axios from 'axios';
// import './App.css';

function App() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rusername, setrUsername] = useState('');
  const [rpassword, setrPassword] = useState('');
  const [loggedInUser, setLoggedInUser] = useState(null);
  const [tenants, setTenants] = useState([]);
  const [selectedTenant, setSelectedTenant] = useState(null);
  const [newTenantName, setNewTenantName] = useState('');
  const [newTenantDomain, setNewTenantDomain] = useState('');
  const [newTenantApiKey, setNewTenantApiKey] = useState('');

  useEffect(() => {
    // check if user is already logged in
    const loggedInUser = localStorage.getItem('loggedInUser');
    if (loggedInUser) {
      setLoggedInUser(JSON.parse(loggedInUser));
    }

    // retrieve all tenants
    axios.get('/tenant')
      .then(response => {
        setTenants(response.data);
      })
      .catch(error => {
        console.error(error);
      });
  }, []);

  const handleRegister = (event) => {
    event.preventDefault();
    axios.post('http://127.0.0.1:5000/register', {
      username: username,
      email: email,
      password: password,
    })
      .then(response => {
        console.log(response.data);
        alert('User registered successfully');
      })
      .catch(error => {
        console.error(error);
        alert('Failed to register user');
      });
  };

  const handleLogin = (event) => {
    event.preventDefault();
    axios.post('http://127.0.0.1:5000/login', {
      rusername: rusername,
      rpassword: rpassword,
    })
      .then(response => {
        console.log(response.data);
        localStorage.setItem('loggedInUser', JSON.stringify(response.data));
        setLoggedInUser(response.data);
        setUsername('');
        setPassword('');
      })
      .catch(error => {
        console.error(error);
        alert('Failed to log in');
      });
  };

  const handleLogout = () => {
    localStorage.removeItem('loggedInUser');
    setLoggedInUser(null);
  };

  const handleCreateTenant = (event) => {
    event.preventDefault();
    axios.post('http://127.0.0.1:5000/tenant', {
      name: newTenantName,
      domain_name: newTenantDomain,
      api_key: newTenantApiKey,
    })
      .then(response => {
        console.log(response.data);
        setTenants([...tenants, {id: response.data.tenant_id, name: newTenantName}]);
        setNewTenantName('');
        setNewTenantDomain('');
        setNewTenantApiKey('');
      })
      .catch(error => {
        console.error(error);
        alert('Failed to create tenant');
      });
  };

  const handleUpdateTenant = (event) => {
    event.preventDefault();
    axios.put(`/tenant/${selectedTenant.id}`, {
      name: selectedTenant.name,
      domain_name: selectedTenant.domain_name,
      api_key: selectedTenant.api_key,
    })
      .then(response => {
        console.log(response.data);
        setTenants(tenants.map(tenant => {
          if (tenant.id === selectedTenant.id) {
            return {...tenant, name: selectedTenant.name};
          } else {
            return tenant;
          }
        }));
        setSelectedTenant(null);
      })
      .catch(error => {
        console.error(error);
        alert('Failed to update tenant');
      });
  };

  const handleDeleteTenant = () => {
    axios.delete(`/tenant/${selectedTenant.id}`)
      .then(response => {
        console.log(response.data);
        setTenants(tenants.filter(tenant => tenant.id !== selectedTenant.id));
        setSelectedTenant(null);
      })
      .catch(error => {
        console.error(error);
        alert('Failed to delete tenant');
      });
  };

  const handleSelectTenant = (tenant) => {
    setSelectedTenant(tenant);
  };

  const handleTenantNameChange = (event) => {
    setSelectedTenant({...selectedTenant, name: event.target.value});
  };

  const handleTenantDomainChange = (event) => {
    setSelectedTenant({...selectedTenant, domain_name: event.target.value});
  };

  const handleTenantApiKeyChange = (event) => {
    setSelectedTenant({...selectedTenant, api_key: event.target.value});
  };

  if (!loggedInUser) {
    return (
      <div className='form-container'>
        <h1>Log in</h1>
        <form onSubmit={handleLogin} className="form-login">
          <div>
            <label htmlFor="username">Username:</label>
            <input type="text" id="username" name="username" value={rusername} onChange={(event) => setrUsername(event.target.value)} />
          </div>
          <div>
            <label htmlFor="password">Password:</label>
            <input type="password" id="password" name="password" value={rpassword} onChange={(event) => setrPassword(event.target.value)} />
          </div>
          <div>
            <button type="submit">Log in</button>
          </div>
        </form>
        
        <h1>Register</h1>
        <form onSubmit={handleRegister} className="form-register">
          <div>
            <label htmlFor="username">Username:</label>
            <input type="text" id="username" name="username" value={username} onChange={(event) => setUsername(event.target.value)} />
          </div>
          <div>
            <label htmlFor="email">Email:</label>
            <input type="email" id="email" name="email" value={email} onChange={(event) => setEmail(event.target.value)} />
          </div>
          <div>
            <label htmlFor="password">Password:</label>
            <input type="password" id="password" name="password" value={password} onChange={(event) => setPassword(event.target.value)} />
          </div>
          <div>
            <button type="submit">Register</button>
          </div>
        </form>


      </div>
    );
  }

  return (
    <div className='App'>
      <div className='container'>
        <div className='row justify-content-center'>
          <div className='col-12 col-md-8 col-lg-6'>
    <div>
      <h1>Welcome, {loggedInUser.username}!</h1>
      <button onClick={handleLogout}>Log out</button>

      <h2>Create a new tenant</h2>
      <form onSubmit={handleCreateTenant}>
        <div>
          <label htmlFor="newTenantName">Name:</label>
          <input type="text" id="newTenantName" name="newTenantName" value={newTenantName} onChange={(event) => setNewTenantName(event.target.value)} />
        </div>
        <div>
          <label htmlFor="newTenantDomain">Domain name:</label>
          <input type="text" id="newTenantDomain" name="newTenantDomain" value={newTenantDomain} onChange={(event) => setNewTenantDomain(event.target.value)} />
        </div>
        <div>
          <label htmlFor="newTenantApiKey">API key:</label>
          <input type="text" id="newTenantApiKey" name="newTenantApiKey" value={newTenantApiKey} onChange={(event) => setNewTenantApiKey(event.target.value)}
          />
        </div>

        <div>
          <button type="submit">Create tenant</button>
        </div>
      </form>

      <h2>Update tenant</h2>
      {selectedTenant && (
        <form onSubmit={handleUpdateTenant}>
          <div>
            <label htmlFor="tenantName">Name:</label>
            <input type="text" id="tenantName" name="tenantName" value={selectedTenant.name} onChange={handleTenantNameChange} />
          </div>
          <div>
            <label htmlFor="tenantDomain">Domain name:</label>
            <input type="text" id="tenantDomain" name="tenantDomain" value={selectedTenant.domain_name} onChange={handleTenantDomainChange} />
          </div>
          <div>
            <label htmlFor="tenantApiKey">API key:</label>
            <input type="text" id="tenantApiKey" name="tenantApiKey" value={selectedTenant.api_key} onChange={handleTenantApiKeyChange} />
          </div>
          <div>
            <button type="submit">Update tenant</button>
            <button onClick={() => setSelectedTenant(null)}>Cancel</button>
            <button onClick={handleDeleteTenant}>Delete tenant</button>
          </div>
        </form>
      )}

      <h2>Tenants</h2>
      <ul>
        {tenants.map(tenant => (
          <li key={tenant.id}>
            <span>{tenant.name}</span>
            <button onClick={() => handleSelectTenant(tenant)}>Edit</button>
          </li>
        ))}
      </ul>
    </div>
  
  /</div>
  </div>
  </div>
  </div>
  );
  
}

export default App;
