<?php
/**
 * @file
 * pfizer_site_module.features.inc
 */

/**
 * Implements hook_ctools_plugin_api().
 */
function pfizer_site_module_ctools_plugin_api($module = NULL, $api = NULL) {
  if ($module == "services" && $api == "services") {
    return array("version" => "3");
  }
}
