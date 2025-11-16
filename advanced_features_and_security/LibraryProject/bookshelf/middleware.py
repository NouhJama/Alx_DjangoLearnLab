"""
Content Security Policy (CSP) Middleware for LibraryProject

This middleware implements Content Security Policy headers to prevent XSS attacks
by controlling which resources (scripts, styles, images, etc.) can be loaded.

Security Benefits:
- Prevents execution of malicious inline scripts
- Controls resource loading from external domains
- Mitigates code injection attacks
- Provides defense-in-depth against XSS vulnerabilities
"""

class CSPMiddleware:
    """
    Custom middleware to add Content Security Policy headers to all responses.
    
    CSP is a security standard that helps prevent XSS attacks by declaring
    which dynamic resources are allowed to load and execute.
    """
    
    def __init__(self, get_response):
        """Initialize the middleware with the next middleware/view in the chain."""
        self.get_response = get_response

    def __call__(self, request):
        """
        Process the request and add CSP headers to the response.
        
        Args:
            request: The HTTP request object
            
        Returns:
            HttpResponse with CSP headers added
        """
        # Get response from the next middleware/view
        response = self.get_response(request)

        # Content Security Policy Configuration
        # Each directive controls a specific type of resource
        csp_directives = [
            # default-src: Default policy for all resource types not explicitly defined
            "default-src 'self'",
            
            # script-src: Controls JavaScript execution
            # 'self': Only allow scripts from same origin
            # 'unsafe-inline' is intentionally NOT included for security
            "script-src 'self'",
            
            # style-src: Controls CSS stylesheets
            # 'self': Same origin stylesheets
            # 'unsafe-inline': Allows inline styles (needed for basic styling)
            # Note: In production, consider moving to external CSS files
            "style-src 'self' 'unsafe-inline'",
            
            # img-src: Controls image sources
            # 'self': Same origin images
            # 'data:': Allows data: URLs for small embedded images
            "img-src 'self' data:",
            
            # font-src: Controls font loading
            "font-src 'self'",
            
            # connect-src: Controls AJAX, WebSocket, and fetch() connections
            "connect-src 'self'",
            
            # object-src: Controls plugins (Flash, etc.)
            # 'none': Disables plugins for security
            "object-src 'none'",
            
            # media-src: Controls audio and video
            "media-src 'self'",
            
            # frame-src: Controls iframe sources
            # 'none': Prevents embedding external content
            "frame-src 'none'",
            
            # base-uri: Controls <base> element URLs
            # 'self': Only allow same-origin base URIs
            "base-uri 'self'",
            
            # form-action: Controls form submission targets
            # 'self': Only allow forms to submit to same origin
            "form-action 'self'",
        ]
        
        # Join all directives with semicolons and add to response
        response["Content-Security-Policy"] = "; ".join(csp_directives)
        
        # Additional security headers for defense-in-depth
        # X-Content-Type-Options: Prevent MIME type sniffing
        response["X-Content-Type-Options"] = "nosniff"
        
        # X-XSS-Protection: Enable browser XSS filtering
        response["X-XSS-Protection"] = "1; mode=block"
        
        # Referrer-Policy: Control referrer information
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"

        return response
