swagger = {
  
  "swagger": "2.0",
  "info": {
    "title": "API Trigger Management",
    "description": "API for managing triggers, logging events, and executing scheduled tasks.",
    "version": "1.0.0"
  },
  "host": "api.example.com",
  "basePath": "/",
  "schemes": ["https"],
  "paths": {
    "/register": {
      "post": {
        "tags": ["User"],
        "summary": "Register a new user.",
        "parameters": [
          {
            "in": "body",
            "name": "body",
            "required": True,
            "schema": {
              "type": "object",
              "properties": {
                "username": {
                  "type": "string",
                  "description": "The username for the new user."
                },
                "password": {
                  "type": "string",
                  "description": "The password for the new user."
                }
              },
              "required": ["username", "password"]
            }
          }
        ],
        "responses": {
          "201": {
            "description": "User registered successfully."
          },
          "400": {
            "description": "Username already exists."
          }
        }
      }
    },
    "/login": {
      "post": {
        "tags": ["User"],
        "summary": "Log in a user and return an access token.",
        "parameters": [
          {
            "in": "body",
            "name": "body",
            "required": True,
            "schema": {
              "type": "object",
              "properties": {
                "username": {
                  "type": "string",
                  "description": "The username of the user."
                },
                "password": {
                  "type": "string",
                  "description": "The password of the user."
                }
              },
              "required": ["username", "password"]
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Login successful, access token returned.",
            "schema": {
              "type": "object",
              "properties": {
                "access_token": {
                  "type": "string",
                  "description": "The JWT access token."
                }
              }
            }
          },
          "401": {
            "description": "Invalid username or password."
          }
        }
      }
    },
    "/scheduled": {
      "get": {
        "tags": ["Trigger"],
        "summary": "Retrieve all scheduled triggers for the authenticated user.",
        "security": [
          {
            "bearerAuth": []
          }
        ],
        "responses": {
          "200": {
            "description": "List of scheduled triggers.",
            "schema": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "id": {
                    "type": "integer",
                    "description": "Trigger ID."
                  },
                  "name": {
                    "type": "string",
                    "description": "Name of the trigger."
                  },
                  "description": {
                    "type": "string",
                    "description": "Description of the trigger."
                  },
                  "schedule_time": {
                    "type": "string",
                    "description": "Time when the trigger is scheduled."
                  }
                }
              }
            }
          }
        }
      },
      "post": {
        "tags": ["Trigger"],
        "summary": "Create a new scheduled trigger.",
        "parameters": [
          {
            "in": "body",
            "name": "trigger",
            "required": True,
            "schema": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "description": "Name of the scheduled trigger."
                },
                "description": {
                  "type": "string",
                  "description": "Description of the trigger."
                },
                "schedule_time": {
                  "type": "string",
                  "description": "Time when the trigger should be executed."
                }
              }
            }
          }
        ],
        "security": [
          {
            "bearerAuth": []
          }
        ],
        "responses": {
          "201": {
            "description": "Scheduled trigger created successfully."
          }
        }
      }
    },
    "/scheduled/{trigger_id}": {
      "delete": {
        "tags": ["Trigger"],
        "summary": "Delete a scheduled trigger by ID.",
        "parameters": [
          {
            "in": "path",
            "name": "trigger_id",
            "required": True,
            "type": "integer",
            "description": "ID of the trigger to delete."
          }
        ],
        "security": [
          {
            "bearerAuth": []
          }
        ],
        "responses": {
          "200": {
            "description": "Trigger deleted successfully."
          },
          "404": {
            "description": "Trigger not found."
          }
        }
      }
    },
    "/api": {
      "get": {
        "tags": ["API Trigger"],
        "summary": "Retrieve all API triggers for the authenticated user.",
        "security": [
          {
            "bearerAuth": []
          }
        ],
        "responses": {
          "200": {
            "description": "List of API triggers.",
            "schema": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "id": {
                    "type": "integer",
                    "description": "API Trigger ID."
                  },
                  "name": {
                    "type": "string",
                    "description": "Name of the API trigger."
                  },
                  "api_url": {
                    "type": "string",
                    "description": "URL of the API."
                  },
                  "method": {
                    "type": "string",
                    "description": "HTTP method for the API request."
                  },
                  "api_payload": {
                    "type": "object",
                    "description": "Payload for the API request."
                  }
                }
              }
            }
          }
        }
      },
      "post": {
        "tags": ["API Trigger"],
        "summary": "Create a new API trigger for the authenticated user.",
        "parameters": [
          {
            "in": "body",
            "name": "api_trigger",
            "required": True,
            "schema": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "description": "Name of the API trigger."
                },
                "api_url": {
                  "type": "string",
                  "description": "URL of the API to trigger."
                },
                "method": {
                  "type": "string",
                  "description": "HTTP method (GET, POST, etc.)."
                },
                "api_payload": {
                  "type": "object",
                  "description": "Payload for the API request."
                }
              }
            }
          }
        ],
        "security": [
          {
            "bearerAuth": []
          }
        ],
        "responses": {
          "201": {
            "description": "API trigger created successfully."
          }
        }
      }
    },
    "/api/{api_trigger_id}": {
      "delete": {
        "tags": ["API Trigger"],
        "summary": "Delete an API trigger by ID.",
        "parameters": [
          {
            "in": "path",
            "name": "api_trigger_id",
            "required": True,
            "type": "integer",
            "description": "ID of the API trigger to delete."
          }
        ],
        "security": [
          {
            "bearerAuth": []
          }
        ],
        "responses": {
          "200": {
            "description": "API trigger deleted successfully."
          },
          "404": {
            "description": "API trigger not found."
          }
        }
      }
    },
    "/events": {
      "get": {
        "tags": ["Event Log"],
        "summary": "Retrieve event logs for the authenticated user.",
        "security": [
          {
            "bearerAuth": []
          }
        ],
        "responses": {
          "200": {
            "description": "List of event logs.",
            "schema": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "id": {
                    "type": "integer",
                    "description": "Event log ID."
                  },
                  "details": {
                    "type": "object",
                    "description": "Details of the event."
                  },
                  "timestamp": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Timestamp of the event."
                  }
                }
              }
            }
          }
        }
      }
    },
    "/execute/{trigger_id}": {
      "post": {
        "tags": ["Trigger Execution"],
        "summary": "Execute the specified trigger.",
        "parameters": [
          {
            "in": "path",
            "name": "trigger_id",
            "required": True,
            "type": "integer",
            "description": "ID of the trigger to execute."
          }
        ],
        "security": [
          {
            "bearerAuth": []
          }
        ],
        "responses": {
          "200": {
            "description": "Trigger execution logged successfully."
          },
          "404": {
            "description": "Trigger not found."
          }
        }
      }
    }
  },
  "securityDefinitions": {
    "bearerAuth": {
      "type": "apiKey",
      "in": "header",
      "name": "Authorization",
      "description": "JWT authorization token"
    }
  }
}


