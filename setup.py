from setuptools import setup, find_packages

setup(
    name="frappe-ev-battery-swap-telematics-engine",
    version="1.0.0",
    description="Frappe EV Fleet Battery Swapping & BMS Telematics Engine: State of Charge (SoC), Thermal Monitoring & Wallet Billing.",
    author="Shyam Kumar Pandey",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False
)
