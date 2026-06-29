function getToken() { return localStorage.getItem('sq_gh_token') || ''; }
function getRailwayUrl() { return (localStorage.getItem('sq_railway_url') || '').replace(/\/$/, ''); }
