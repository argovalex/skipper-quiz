function getToken() { return localStorage.getItem('sq_gh_token') || ''; }
function getRailwayUrl() {
  let u = (localStorage.getItem('sq_railway_url') || '').trim().replace(/\/$/, '');
  if (u && !/^https?:\/\//i.test(u)) u = 'https://' + u; // a scheme-less value is treated by fetch() as a relative path → "Failed to fetch"
  return u;
}
