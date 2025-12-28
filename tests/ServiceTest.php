<?php

namespace Neucore\Plugin\Mumble\Tests;

use Neucore\Plugin\Data\PluginConfiguration;
use Neucore\Plugin\Mumble\Service;
use Neucore\Plugin\ServiceInterface;
use PHPUnit\Framework\TestCase;

class ServiceTest extends TestCase
{
    public function testConstruct()
    {
        $implementation = new Service(
            new TestLogger(),
            new PluginConfiguration(0, '', true, [], ''),
            new TestFactory()
        );
        /** @noinspection PhpConditionAlreadyCheckedInspection */
        $this->assertInstanceOf(ServiceInterface::class, $implementation);
    }
}
