# Design Considerations

When choosing the right design for this application I considered 2 approaches. These were monolithic vs microservice architecture. Below are the pros and cons of each. 
Ultimately as I chose to prioritise simplicity, readability, and clean best practices, a **monolithic architecture** seems most suitable. It offers a straightforward development and deployment process, which is ideal for a project of this scope. I can always refactor into microservices later as the project grows, if necessary.

### **Monolithic Architecture**

**Pros:**

1. **Simplicity:** Easier to develop, test, deploy, and run, especially for small to medium-sized applications.
2. **Unified Development:** All parts of the application are developed in a single codebase, simplifying development and deployment processes.
3. **Less Operational Overhead:** Doesn't require managing a complex network of services, which is ideal for smaller teams or projects.

**Cons:**

1. **Scalability Issues:** Scaling a monolithic application can be challenging, especially if different modules have different resource requirements.
2. **Tight Coupling:** Changes in one part of the system can impact other parts, leading to a higher risk of unexpected issues.
3. **Limited Technology Flexibility:** You're generally locked into the tech stack you start with.

### **Microservices Architecture**

**Pros:**

1. **Scalability:** Easier to scale and manage parts of the application independently.
2. **Flexibility:** Each service can use a technology stack that best suits its needs.
3. **Resilience:** Failure in one service doesn't necessarily bring down the entire application.

**Cons:**

1. **Complexity:** More complex to develop, deploy, and manage due to distributed nature.
2. **Resource Intensive:** Requires more resources, both in terms of infrastructure and development effort.
3. **Testing Challenges:** Integration and end-to-end testing can be more complicated.

### **Serverless Architecture (Alternative Approach)**

Serverless architecture involves running applications without managing servers, typically on cloud platforms like AWS Lambda, Azure Functions, or Google Cloud Functions.

**Pros:**

1. **Operational Efficiency:** No server management; you're only charged for the compute time you use.
2. **Scalability:** Automatically scales based on the workload.
3. **Rapid Deployment:** Allows for quick iterations and deployments.

**Cons:**

1. **Vendor Lock-In:** Reliant on cloud providers and their limitations.
2. **Performance Issues:** Can suffer from cold starts (initial delay when the function is not 'warm').
3. **Complex State Management:** Managing state and data across function invocations can be challenging.