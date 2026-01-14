class ApiError extends Error {
    /**
     * Error object containing response status, error code, and error message
     */
    constructor(status, { error, message }) {
      super(message);
      this.status = status;
      this.code = error;
    }
  }
  const baseUrl = os.getenv("API_URL") 

  
  const handleResponse = async (response) => {
    if (response.ok) {
      return response.status == 204 ? {} : await response.json();
    } else {
      const error = await response.json();
      if (error.detail) {
        throw new ApiError(response.status, {
          error: "validation",
          message: JSON.stringify(error.detail),
        });
      } else {
        throw new ApiError(response.status, error);
      }
    }
  };
  
  const get = async (url, headers) => {
    const response = await fetch(baseUrl + url, { headers: headers, });
    return await handleResponse(response);
  };

  const put = async (url, headers, data) => {
    const response = await fetch(baseUrl + url, {
      headers,
      method: "PUT",
      body: JSON.stringify(data),
    });
    return await handleResponse(response);
  };
  
  const post = async (url, headers, data) => {
    const response = await fetch(baseUrl + url, {
      headers,
      method: "POST",
      body: JSON.stringify(data),
    });
    return await handleResponse(response);
  };
  
  const form = async (url, headers, data) => {
    const response = await fetch(baseUrl + url, {
      headers: {
        ...headers,
        "Content-Type": "application/x-www-form-urlencoded",
      },
      method: "POST",
      body: new URLSearchParams(data),
    });
    return await handleResponse(response);
  };

  const putForm = async (url, headers, data) => {
    const response = await fetch(baseUrl + url, {
      headers: {
        ...headers,
        "Content-Type": "application/x-www-form-urlencoded",
      },
      method: "PUT",
      body: new URLSearchParams(data),
    });
    return await handleResponse(response);
  };
  
  const _delete = async (url, headers) => {
    const response = await fetch(baseUrl + url, {
      headers: {
        ...headers,
      },
      method: "DELETE",
    });
    return await handleResponse(response);
  }

  export default { get, put, post, form, _delete, putForm };
  