import os
import logging
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "tlc-business-solutions-secret")

# Configure for proxy headers
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Disable caching for all requests
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Add global context processor to make current year available to all templates
@app.context_processor
def inject_now():
    return {'now': datetime.datetime.now()}

@app.route('/')
def index():
    return render_template('index.html', active_page='home')

@app.route('/features')
def features():
    return render_template('features.html', active_page='features')

@app.route('/about')
def about():
    return render_template('about.html', active_page='about')

@app.route('/financial-snapshot', methods=['GET', 'POST'])
def financial_snapshot():
    if request.method == 'POST':
        # Get form data
        monthly_revenue = float(request.form.get('monthly_revenue', 0))
        monthly_expenses = float(request.form.get('monthly_expenses', 0))
        outstanding_invoices = float(request.form.get('outstanding_invoices', 0))
        accounts_payable = float(request.form.get('accounts_payable', 0))
        cash_reserves = float(request.form.get('cash_reserves', 0))
        
        # Calculate key metrics
        profit_margin = ((monthly_revenue - monthly_expenses) / monthly_revenue * 100) if monthly_revenue > 0 else 0
        cash_flow = monthly_revenue - monthly_expenses
        runway_months = (cash_reserves / monthly_expenses) if monthly_expenses > 0 else 0
        accounts_receivable_ratio = (outstanding_invoices / monthly_revenue) if monthly_revenue > 0 else 0
        debt_to_income = (accounts_payable / monthly_revenue) if monthly_revenue > 0 else 0
        
        # Define health indicators
        profit_health = "Healthy" if profit_margin >= 20 else "Caution" if profit_margin >= 10 else "Attention Needed"
        cash_flow_health = "Healthy" if cash_flow > 0 else "Attention Needed"
        runway_health = "Healthy" if runway_months >= 3 else "Caution" if runway_months >= 1 else "Attention Needed"
        receivable_health = "Healthy" if accounts_receivable_ratio <= 1 else "Caution" if accounts_receivable_ratio <= 2 else "Attention Needed"
        debt_health = "Healthy" if debt_to_income <= 0.5 else "Caution" if debt_to_income <= 1 else "Attention Needed"
        
        # Calculate overall financial health score (simple average of the 5 metrics)
        score_mapping = {"Healthy": 3, "Caution": 2, "Attention Needed": 1}
        health_score = (score_mapping[profit_health] + score_mapping[cash_flow_health] + 
                         score_mapping[runway_health] + score_mapping[receivable_health] + 
                         score_mapping[debt_health]) / 5 * 100 / 3  # Convert to percentage
        
        # Prepare results to pass to template
        snapshot_results = {
            'profit_margin': profit_margin,
            'cash_flow': cash_flow,
            'runway_months': runway_months,
            'accounts_receivable_ratio': accounts_receivable_ratio,
            'debt_to_income': debt_to_income,
            'profit_health': profit_health,
            'cash_flow_health': cash_flow_health,
            'runway_health': runway_health,
            'receivable_health': receivable_health,
            'debt_health': debt_health,
            'health_score': health_score
        }
        
        return render_template('financial_snapshot.html', active_page='financial_snapshot', 
                              snapshot_results=snapshot_results, show_results=True)
    
    return render_template('financial_snapshot.html', active_page='financial_snapshot', show_results=False)

@app.route('/contact')
def contact():
    return render_template('contact.html', active_page='contact')

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        
        # Here you would typically send an email or store the contact form data
        # For now, just log the data
        app.logger.info(f"Contact form submission: {name}, {email}, {phone}, {message}")
        
        # Flash a success message
        flash('Thank you for contacting us! We will be in touch shortly.', 'success')
        
        # Redirect to thank you page
        return render_template('thank_you.html', name=name)
    
    return redirect(url_for('contact'))

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('base.html', title='404 - Page Not Found', 
                          error_message='The page you are looking for does not exist.'), 404

# Test route for images
@app.route('/test-images')
def test_images():
    return render_template('test_images.html')

# Charge calculator functions
def calculate_charge_rate(form_data):
    # Initialize results dictionary
    results = {}
    
    # OVERHEAD CALCULATIONS (First sheet)
    # Get overhead inputs from form
    try:
        # Helper function to safely convert form values to float
        def safe_float(value, default=0):
            if value is None or value == '':
                return default
            try:
                return float(value)
            except ValueError:
                return default
        
        # Helper function to safely convert form values to int
        def safe_int(value, default=0):
            if value is None or value == '':
                return default
            try:
                return int(value)
            except ValueError:
                return default
        
        # Annual overheads
        rent = safe_float(form_data.get('rent'))
        utilities = safe_float(form_data.get('utilities'))
        insurance = safe_float(form_data.get('insurance'))
        office_expenses = safe_float(form_data.get('office_expenses'))
        marketing = safe_float(form_data.get('marketing'))
        vehicle_expenses = safe_float(form_data.get('vehicle_expenses'))
        equipment = safe_float(form_data.get('equipment'))
        software_subscriptions = safe_float(form_data.get('software_subscriptions'))
        professional_services = safe_float(form_data.get('professional_services'))
        other_overheads = safe_float(form_data.get('other_overheads'))
        
        # Total annual overheads
        total_overheads = (rent + utilities + insurance + office_expenses + marketing + 
                          vehicle_expenses + equipment + software_subscriptions + 
                          professional_services + other_overheads)
        
        # LABOR COSTS CALCULATIONS (Second sheet)
        # Owner information
        owner_annual_drawings = safe_float(form_data.get('owner_annual_drawings'))
        owner_billable_hours_percent = safe_float(form_data.get('owner_billable_hours_percent'), 50) / 100
        
        # Employee information
        employee_count = safe_int(form_data.get('employee_count'))
        average_employee_salary = safe_float(form_data.get('average_employee_salary'))
        employee_billable_hours_percent = safe_float(form_data.get('employee_billable_hours_percent'), 70) / 100
        
        # Working hours
        annual_weeks_worked = safe_float(form_data.get('annual_weeks_worked'), 48)
        weekly_working_hours = safe_float(form_data.get('weekly_working_hours'), 40)
        
        # Calculate totals
        annual_working_hours = annual_weeks_worked * weekly_working_hours
        
        # Owner billable hours
        owner_billable_hours = annual_working_hours * owner_billable_hours_percent
        owner_labor_cost = owner_annual_drawings
        
        # Employee billable hours
        if employee_count > 0:
            employee_total_cost = employee_count * average_employee_salary
            employee_billable_hours = employee_count * annual_working_hours * employee_billable_hours_percent
        else:
            employee_total_cost = 0
            employee_billable_hours = 0
        
        # Total billable hours and labor costs
        total_billable_hours = owner_billable_hours + employee_billable_hours
        total_labor_cost = owner_labor_cost + employee_total_cost
        
        # CHARGE RATE CALCULATIONS
        # Profit targets
        profit_margin_percent = safe_float(form_data.get('profit_margin_percent'), 20) / 100
        annual_profit_target = safe_float(form_data.get('annual_profit_target'))
        
        # If user specifies annual profit target, use that
        if annual_profit_target > 0:
            total_revenue_needed = total_overheads + total_labor_cost + annual_profit_target
            profit_amount = annual_profit_target
        else:
            # Otherwise use profit margin percentage
            base_costs = total_overheads + total_labor_cost
            # Avoid division by zero
            if profit_margin_percent >= 1:
                profit_margin_percent = 0.99  # Cap at 99%
            
            profit_amount = base_costs * profit_margin_percent / (1 - profit_margin_percent)
            total_revenue_needed = base_costs + profit_amount
        
        # Calculate hourly charge rate
        if total_billable_hours > 0:
            hourly_charge_rate = total_revenue_needed / total_billable_hours
        else:
            hourly_charge_rate = 0
        
        # Ensure we have a valid calculation
        if total_overheads == 0 and total_labor_cost == 0:
            raise ValueError("Please enter at least some business costs or labor costs to calculate a charge rate")
        
        # Store all calculations in results
        results = {
            # Overhead totals
            'total_overheads': total_overheads,
            
            # Billable hours
            'annual_working_hours': annual_working_hours,
            'owner_billable_hours': owner_billable_hours,
            'employee_billable_hours': employee_billable_hours,
            'total_billable_hours': total_billable_hours,
            
            # Labor costs
            'owner_labor_cost': owner_labor_cost,
            'employee_total_cost': employee_total_cost,
            'total_labor_cost': total_labor_cost,
            
            # Profit and revenue
            'profit_amount': profit_amount,
            'total_revenue_needed': total_revenue_needed,
            
            # Final charge rate
            'hourly_charge_rate': hourly_charge_rate,
            
            # Success flag
            'calculation_success': True
        }
    except Exception as e:
        # If any calculations fail, return error
        app.logger.error(f"Calculation error: {str(e)}")
        # Use a minimal error message
        results = {
            'calculation_success': False,
            'error_message': "Please check your inputs and try again."
        }
    
    return results

# Charge calculator route
@app.route('/charge-calculator', methods=['GET', 'POST'])
def charge_calculator():
    if request.method == 'POST':
        # Process form data and calculate results
        results = calculate_charge_rate(request.form)
        
        if results['calculation_success']:
            # If calculation was successful, render the results page with the form data
            return render_template('calculator_results.html', active_page='calculator', results=results, form_data=request.form)
        else:
            # If there was an error, go back to the calculator with the error message
            return render_template('charge_calculator.html', active_page='calculator', results=results, form_data=request.form)
    
    # Default GET request - render the calculator form
    return render_template('charge_calculator.html', active_page='calculator')

# Route to serve domain verification files
@app.route('/.well-known/<path:filename>')
def well_known(filename):
    app.logger.info(f"Accessing .well-known file: {filename}")
    return send_from_directory('static/.well-known', filename)

@app.errorhandler(500)
def server_error(e):
    return render_template('base.html', title='500 - Server Error',
                          error_message='Something went wrong on our end. Please try again later.'), 500